# 데이터 분석 준비
import pandas as pd
import numpy as np

# 데이터 로딩
print("데이터 로딩 중...")
EPL_test = pd.read_csv('./datasets/test20_22.csv', encoding='cp949')
print("데이터 로딩 완료")

from sklearn.model_selection import train_test_split
# 필요한 feature만 뽑아 새로운 df에 저장 
# 풀타임 결과(H, D, R), 슈팅수, 유효슈팅수, 파울, 코너킥, 옐로카드, 레드카드
EPL_test_ext = EPL_test[['FTR', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF',
                     'HC', 'AC', 'HY', 'AY', 'HR', 'AR']]


# # EPL_test_ext = EPL_test_ext[EPL_test_ext.FTR != 'D']
# EPL_test_ext['RESULT'] = np.where(EPL_test_ext['FTR']=='H', 1, 0)
EPL_test_ext.loc[EPL_test_ext.FTR=="H", 'RESULT'] = "1"
EPL_test_ext.loc[EPL_test_ext.FTR=="A", 'RESULT'] = "-1"
EPL_test_ext.loc[EPL_test_ext.FTR=="D", 'RESULT'] = "0"
EPL_test_ext.drop('FTR', axis=1, inplace=True)
print(EPL_test_ext)

# 데이터 내에서 학습 집합과 테스트 집합을 나눔(8:2)
# train, test = train_test_split(EPL_df_ext, test_size=0.2, random_state=12)
test = EPL_test_ext

X_test = test.drop("RESULT", axis=1)
Y_test = test["RESULT"]

import joblib
print("logreg-model.joblib에서 모델을 불러오는 중....")
logreg = joblib.load("logreg-model.joblib")
print("완료")
Y_pred_logreg = logreg.predict(X_test)

acc_log = logreg.score(X_test, Y_test)

print(f'accuracy: {acc_log: .4f}')

import pickle
with open("match_data.pickle", "rb") as f:
    input_data = pickle.load(f)

from datetime import datetime
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
aaa = obtain_exponential_mean(input_data[('Everton', 'West Brom')], 0.2)