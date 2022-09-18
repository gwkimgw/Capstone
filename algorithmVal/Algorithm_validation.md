# Algorithm validation

### Reference

---

- 참고 논문 및 사이트
    - [https://medium.com/@bjmoon.korea/ai-x-딥러닝-fianl-assignment-84e66d7e451d](https://medium.com/@bjmoon.korea/ai-x-%EB%94%A5%EB%9F%AC%EB%8B%9D-fianl-assignment-84e66d7e451d)
    - 
        
        [applsci-10-06750-v2.pdf](Algorithm%20validation%2044471cd2e7f84510a18800c264237e66/applsci-10-06750-v2.pdf)
        
    
- 읽어봐야 할 논문 및 사이트
    - [https://github.com/mikha122/mypojects/tree/main/Football Project](https://github.com/mikha122/mypojects/tree/main/Football%20Project)
    - feature selection
        - [https://dyddl1993.tistory.com/18](https://dyddl1993.tistory.com/18)

### 생각해보기

---

1. 같은 feature를 사용, 다른 알고리즘으로 검증
    - [x]  같은 feature를 사용해서 알고리즘 돌려보기
2. 다른 feature를 사용, 같은 알고리즘 검증
    - [ ]  다른 feature를 사용해서 같은 알고리즘끼리 비교하기
    - [ ]  feature 선정은 어떻게?
    - [ ]  추가적으로 수집할 데이터 있는지 알아보기
3. 1,2번을 조합해서 가장 정확도가 높은 feature와 알고리즘 찾기
    - [ ]  1, 2번을 조합해서 가장 정확도가 높은 feature와 알고리즘을 찾기
    - [ ]  알고리즘 보완하기
4. 마냥 많은 season을 사용한 모델이 좋을까?

### 사용할 feature 정하기

---

일단 알고리즘을 찾아보자

- [x]  Random Forest: `accuracy:  0.7697`
- [x]  xgboost: `accuracy:  0.7715`
- [x]  Support Vector Machines: `accuracy:  0.7903`
- [x]  Logistic Regression: `accuracy:  0.7903`
- [x]  K-Nearest Neighbor: `accuracy:  0.6966`
- [x]  Naive Bayes classifiers: `accuracy:  0.7154`
- [x]  Decision Tree: `accuracy:  0.7004`
- [x]  Artificial Neural Network: `accuracy:  0.7715`
- [x]  Keras: ANN model: `accuracy:  0.7604`

# Algorithm Validation

---

# Datasets

---

- EPL_prediciton_data.csv
    
    ~~League~~
    
    MatchID
    
    Match_Date
    
    Home_Name
    
    Away_Name
    
    Home_GF
    
    Away_GF
    
    Result
    
    Season
    
    Home_IAR
    
    Away_IAR
    
    Home_IN
    
    Away_IN
    
    Home_WIN6
    
    DRAW6
    
    Home_LOSE6
    
    HWS
    
    AWS
    
    HLS
    
    ALS
    
    RVD
    
    odds_w
    
    odds_d
    
    odds_l
    
    RMPE5
    
    GCR_3
    
    SoT_3
    
    ADS_3
    
    PS_3
    
    Pass_3
    
    Pass_DIR_For_3
    
    Pass_For_Ratio_3
    
    Pass_TZ_MT_3
    
    Pass_TZ_FT_3
    
    Pass_MT_Ratio_3
    
    Pass_FT_Ratio_3
    
    Pass_Long_3
    
    Pass_Long_ratio_3
    
    Dribble_3
    
    Dribble_ratio_3
    
    Intercept_by_pass_3
    
    Clear_by_pass_3
    
    pass_by_Intercept_3
    
    pass_by_Clear_3
    
    LOP_by_touch_3
    
    Shots_3
    
    OP_3
    
    CA_3
    
    CR_3
    
    Tackles_3
    
    RATE_3
    
    Touch_3
    
    Save_ratio_3
    
- result2.csv
    
    Season: Match Season
    
    DateTime: Match date and time ( yyyy-mm -dd hh:mm:ss)
    
    HomeTeam
    
    AwayTeam
    
    FTHG: Full time home team goals
    
    FTAG: Full time away team goals
    
    FTR: Full time result(H, D, A)
    
    HTHG: Half time home team goals
    
    HTAG: Half time away team goals
    
    HTR: Half time result(H, D, A)
    
    Referee: 
    
    HS: Home team shots
    
    AS: Away team shots
    
    HST: Home Team shots on target
    
    AST: Away team shots on target
    
    HC: home team corners
    
    AC: away team corners
    
    HF: home team fouls committed
    
    AF: away team fouls committed
    
    HY: Home team Yellow Card
    
    AY: Away team Yellow Card
    
    HR: Home Team Red Card
    
    AR: Away team Red Card
    

# **validation baseline system**

---

### Installation

- conda 환경 셋팅
    
    [requirements.txt](Algorithm%20validation%2044471cd2e7f84510a18800c264237e66/requirements.txt)
    
- jupyter notebook
    
    [EPL_validation.ipynb](Algorithm%20validation%2044471cd2e7f84510a18800c264237e66/EPL_validation.ipynb)
    
    [EPL_validation_2.ipynb](Algorithm%20validation%2044471cd2e7f84510a18800c264237e66/EPL_validation_2.ipynb)
    

### **Description**

- 사용 데이터: result2.csv
    - 데이터 전처리
        
        Season: Match Season
        
        DateTime: Match date and time ( yyyy-mm -dd hh:mm:ss)
        
        HomeTeam
        
        AwayTeam
        
        FTHG: Full time home team goals
        
        FTAG: Full time away team goals
        
        **FTR: Full time result(H, D, A)**
        
        HTHG: Half time home team goals
        
        HTAG: Half time away team goals
        
        HTR: Half time result(H, D, A)
        
        Referee: 
        
        **HS: Home team shots**
        
        **AS: Away team shots**
        
        **HST: Home Team shots on target**
        
        **AST: Away team shots on target**
        
        **HC: home team corners**
        
        **AC: away team corners**
        
        **HF: home team fouls committed**
        
        **AF: away team fouls committed**
        
        **HY: Home team Yellow Card**
        
        **AY: Away team Yellow Card**
        
        **HR: Home Team Red Card**
        
        **AR: Away team Red Card**
        
- FTR를 binary 형태로 변환(무승부 제거)
    - H: 1, A: 0

### Algorithm - 설명 추가 필요

- Random Forest
- Xgboost
- SVM
- Logistic Regression
- k-Nearest Neighbor: [https://hleecaster.com/ml-knn-concept/](https://hleecaster.com/ml-knn-concept/)
- Naive Bayes classifiers
- Decision Tree
- ANN

## 선택한 알고리즘

---

선택한 이유 서술