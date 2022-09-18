# 데이터 분석 준비
import pandas as pd
import numpy as np

# 데이터 로딩
print("데이터 로딩 중...")
EPL_df = pd.read_csv('./datasets/results_00_19.csv', encoding='cp949')
EPL_test = pd.read_csv('./datasets/test20_22.csv', encoding='cp949')
print("데이터 로딩 완료")

print(EPL_df.columns.values)
print(EPL_df.head())
print(EPL_df.info()) # null 값 존재 x
print(EPL_df.describe())
print(EPL_df.isnull().sum())
print(EPL_df[EPL_df.DateTime.isnull()])
EPL_df = EPL_df.dropna()

# 홈팀 어웨이팀으로 나뉘어있는 feature를 분석하기 좋게 하나의 새로운 feature로 표현
EPL_df['DIFF_FG'] = EPL_df['FTHG'] - EPL_df['FTAG'] # 홈팀 풀타임 골 - 어웨이팀 풀타임 골
EPL_df['DIFF_HG'] = EPL_df['HTHG'] - EPL_df['HTAG'] # 홈팀 하프타임 골 - 어웨이팀 하프타임 골
EPL_df['DIFF_SHOOT'] = EPL_df['HS'] - EPL_df['AS'] # 홈팀 슈팅 수 - 어웨이팀 슈팅 수 
EPL_df['DIFF_ST'] = EPL_df['HST'] - EPL_df['AST'] # 홈팀 유효슈팅 수 - 어웨이팀 유효슈팅 수
EPL_df['DIFF_FOUL'] = EPL_df['HF'] - EPL_df['AF'] # 홈팅 파울 - 어웨이팀 파울
EPL_df['DIFF_CONER'] = EPL_df['HC'] - EPL_df['AC'] # 홈팀 코너킥 - 어웨팀 코너킥
EPL_df['DIFF_YC'] = EPL_df['HY'] - EPL_df['AY'] # 홈팀 옐로카드 - 어웨이팀 옐로카드
EPL_df['DIFF_RC'] = EPL_df['HR'] - EPL_df['AR'] # 홈팀 레드카드 - 어웨이팀 레드카드

list_dif = ["FTR", "DIFF_FG", "DIFF_HG", "DIFF_SHOOT","DIFF_ST","DIFF_FOUL","DIFF_CONER","DIFF_YC","DIFF_RC"]
EPL_df[list_dif].groupby(['FTR'], as_index=False).mean().sort_values(by='FTR', ascending=False)

from sklearn.model_selection import train_test_split
# 필요한 feature만 뽑아 새로운 df에 저장 
# 풀타임 결과(H, D, R), 슈팅수, 유효슈팅수, 파울, 코너킥, 옐로카드, 레드카드
EPL_df_ext = EPL_df[['FTR', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF',
                     'HC', 'AC', 'HY', 'AY', 'HR', 'AR']]
EPL_test_ext = EPL_test[['FTR', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF',
                     'HC', 'AC', 'HY', 'AY', 'HR', 'AR']]
print(EPL_df_ext)

# FTR 무승부 지우고 binary 형태로
# 무승부 경기를 제외하고 홈팀이 이긴 것을 RESULT의 1로 
# EPL_df_ext = EPL_df_ext[EPL_df_ext.FTR != 'D']
# EPL_df_ext['RESULT'] = np.where(EPL_df_ext['FTR']=='H', 1, 0)
EPL_df_ext.loc[EPL_df_ext.FTR=="H", 'RESULT'] = "1"
EPL_df_ext.loc[EPL_df_ext.FTR=="A", 'RESULT'] = "-1"
EPL_df_ext.loc[EPL_df_ext.FTR=="D", 'RESULT'] = "0"
EPL_df_ext.drop('FTR', axis=1, inplace=True)
print(EPL_df_ext)

# # EPL_test_ext = EPL_test_ext[EPL_test_ext.FTR != 'D']
# EPL_test_ext['RESULT'] = np.where(EPL_test_ext['FTR']=='H', 1, 0)
EPL_test_ext.loc[EPL_test_ext.FTR=="H", 'RESULT'] = "1"
EPL_test_ext.loc[EPL_test_ext.FTR=="A", 'RESULT'] = "-1"
EPL_test_ext.loc[EPL_test_ext.FTR=="D", 'RESULT'] = "0"
EPL_test_ext.drop('FTR', axis=1, inplace=True)
print(EPL_test_ext)

# 데이터 내에서 학습 집합과 테스트 집합을 나눔(8:2)
# train, test = train_test_split(EPL_df_ext, test_size=0.2, random_state=12)
train = EPL_df_ext
test = EPL_test_ext

X_train = train.drop("RESULT", axis=1) # 열 지움
Y_train = train["RESULT"]
X_test = test.drop("RESULT", axis=1)
Y_test = test["RESULT"]
X_train.shape, Y_train.shape, X_test.shape, Y_test.shape
print(X_train)

from sklearn.linear_model import LogisticRegression 

# 수정
# Logistic Regression training
logreg = LogisticRegression(solver='liblinear')
logreg.fit(X_train, Y_train)
# Logistic Regression prediction
Y_pred_logreg = logreg.predict(X_test)

acc_log = logreg.score(X_test, Y_test)

print(f'accuracy: {acc_log: .4f}')

import joblib
print("logreg-model.joblib으로 모델을 저장 중....")
joblib.dump(logreg, "logreg-model.joblib")
print("완료")