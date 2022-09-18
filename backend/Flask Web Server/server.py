from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user, logout_user
from flask_login import current_user
from datetime import datetime
import numpy
import sqlite3
import pathlib
import joblib
import pickle
import pandas as pd
import secrets

app = Flask(__name__)

# 비밀키 불러오기
# 없으면 현재 폴더의 secretkey 파일을 생성, 있으면 거기서 불러옴
secretkey_file = pathlib.Path("./secretkey")
try:
    with secretkey_file.open() as f:
        app.secret_key = f.read().strip()
except FileNotFoundError:
    generated_secret_key = secrets.token_hex()
    with secretkey_file.open(mode="w") as f:
        f.write(generated_secret_key)
    app.secret_key = generated_secret_key

# 패스워드 해시 salt 값 불러오기
pwdsalt_file = pathlib.Path("./passwordsalt")
try:
    with pwdsalt_file.open() as f:
        password_salt = f.read().strip()
except FileNotFoundError:
    password_salt = secrets.token_hex()
    with pwdsalt_file.open(mode="w") as f:
        f.write(password_salt)

# flask-login 설정
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = "/login"

# 유저 정보 DB 초기화
db_conn = sqlite3.connect("user.db")
db_conn.execute("""
CREATE TABLE IF NOT EXISTS
userdata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(256) UNIQUE,
    password CHAR(64),
    salt CHAR(64)
);
""")
db_conn.commit()
db_conn.close()

# 유저 로그인 정보를 나타내는 클래스
# flask-login이 요구하는 형식에 맞춰야 함 (자세한 건 공식 문서 참고)
class User:
    def __init__(self, uid):
        self.uid = uid

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.uid

@login_manager.user_loader
def load_user(user_id):
    db_conn = sqlite3.connect("user.db")
    cur = db_conn.execute("""
    SELECT * FROM userdata WHERE id = {};
    """.format(int(user_id)))
    data = cur.fetchall()
    db_conn.close()
    if not data:
        return None
    return User(user_id)

def obtain_exponential_mean(data_list, coeff):
    data_list = [i.copy() for i in data_list]
    for i in data_list:
        i["DateTime"] = datetime.fromisoformat(i["DateTime"].strip('Z'))
    data_list.sort(key=lambda x: x["DateTime"])
    result = data_list.pop(0)
    result.pop("DateTime")
    for i in data_list:
        for k in result:
            result[k] = float(result[k])*(1-coeff) + float(i[k])*coeff
    return pd.DataFrame([result])

@app.route("/get-prediction", methods=["GET", "POST"])
def get_prediction():
    if not current_user.is_authenticated:
        return {"authorized": False, "result": None}
    # if request.method == "GET":
    #     화면 렌더링 로직이 들어가야 함.
    #     home = request.args["home"]
    #     away = request.args["away"]
    #     coeff = float(request.args["coeff"])
    elif request.method == "POST":
        home = request.form["home"]
        away = request.form["away"]
        coeff = 0.3
    logreg = joblib.load("logreg-model.joblib")
    with open("match_data.pickle", "rb") as f:
        input_data = pickle.load(f)
    if (home, away) not in input_data:
        result = None
    else:
        mean_value = obtain_exponential_mean(input_data[(home,away)], coeff)
        result = numpy.round(logreg.predict_proba(mean_value).tolist(),2) * 100
        print(result)
    # return {"authorized": True, "result": result[0] if result is not None else None}
    return render_template("result.html", result = result[0] if result is not None else None, home = home, away = away)

@app.route("/")
def index_world():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login_world():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        req_data = request.get_json()
        username = req_data["username"]
        password = req_data["password"]

        # 유저 이름이 비어있지 않은지 검사
        if len(username) == 0:
            return {
                "login_success": False,
                "reason": "잘못된 유저 이름입니다. (유저 이름이 비어있습니다)"
            }

        # 유저 이름이 [A-Za-z0-9]로만 이루어져 있는지 검사
        import string
        allowed_chars = string.ascii_letters + string.digits
        for i in username:
            if i not in allowed_chars:
                return {
                    "login_success": False,
                    "reason": "잘못된 유저 이름입니다. (영대소문자와 숫자로만 이루어져야 함)"
                }

        # DB에서 유저 데이터 불러오기
        db_conn = sqlite3.connect("user.db")
        cur = db_conn.execute("""
        SELECT id, username, password, salt
        FROM userdata WHERE username = '{}';
        """.format(username))
        data = cur.fetchall()
        db_conn.close()
        if not data:
            return {
                "login_success": False,
                "reason": "유저가 존재하지 않거나 패스워드가 잘못되었습니다."
            }
        
        # 유저 패스워드 검사
        salted = password + data[0][3]
        import hashlib
        digest = hashlib.sha256(salted.encode(encoding="utf-8")).hexdigest()
        if digest != data[0][2]:
            return {
                "login_success": False,
                "reason": "유저가 존재하지 않거나 패스워드가 잘못되었습니다."
            }

        # 전부 통과함; 로그인 실행
        login_user(User(data[0][0]))
        return {"login_success": True, "reason": "로그인 성공"}
    return render_template("login.html")

@app.route("/signup", methods=["POST"])
def signup_world():
    req_data = request.get_json()
    username = req_data["username"]
    password = req_data["password"]

    # 유저 이름이 [A-Za-z0-9]로만 이루어져 있는지 검사
    import string
    allowed_chars = string.ascii_letters + string.digits
    for i in username:
        if i not in allowed_chars:
            return {
                "signup_success": False,
                "reason": "잘못된 유저 이름입니다. (영대소문자와 숫자로만 이루어져야 함)"
            }

    # DB에서 유저 데이터 불러오기
    db_conn = sqlite3.connect("user.db")
    cur = db_conn.execute("""
    SELECT id, username, password, salt
    FROM userdata WHERE username = '{}';
    """.format(username))
    data = cur.fetchall()
    db_conn.close()
    if data:
        return {
            "signup_success": False,
            "reason": "해당 아이디를 가진 유저가 이미 존재합니다."
        }

    # 패스워드가 조건을 만족하는지 검사
    if len(password) < 8:
        return {
            "signup_success": False,
            "reason": "비밀번호는 8자리 이상이여야 합니다."
        }
    allowed_chars = string.ascii_letters + string.digits
    for i in password:
        if i not in allowed_chars:
            return {
                "signup_success": False,
                "reason": "비밀번호는 영대소문자와 숫자로만 이루어져 있어야 합니다."
            }
        
    # 유저 패스워드 해싱
    salt = secrets.token_hex()
    salted = password + salt
    import hashlib
    digest = hashlib.sha256(salted.encode(encoding="utf-8")).hexdigest()

    # 유저 등록
    db_conn = sqlite3.connect("user.db")
    cur = db_conn.execute("""
    INSERT INTO userdata (username, password, salt)
    VALUES ('{0}', '{1}', '{2}');
    """.format(username, digest, salt))
    db_conn.commit()
    db_conn.close()

    return {"signup_success": True, "reason": "Sign-up successful"}

@app.route("/logout")
def logout_world():
    logout_user()
    return redirect("/")


@app.route("/predict")
def predict():
    return render_template("predict.html")

if __name__ == '__main__':
   app.run(debug = True)
