# -*- coding: utf-8 -*-
"""ETL실습_김효관.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bZiEndPyfPdzC_NS3WX6iooFz4p9wFqJ
"""

# !pip install mysql-connector-python

"""# 라이브러리 선언"""

# Pandas 패키지 불러오기
from sqlalchemy import create_engine, inspect
import pandas as pd
import requests, bs4
from datetime import datetime

"""# 1. 파이썬 기초다기지 리마인드겸 확인

tvList2 = [ 'UN40EN001', 'UN40EN002’,
'UN40EN003', 'UN40EN004’]
모든 리스트의 앞에 "LEDTV_"를 붙인다!!
"""

# tvList2 = [ 'UN40EN001', 'UN40EN002', 'UN40EN003', 'UN40EN004']
# ### STEP1: 접두어를 선언한다 "LEDTV_"
# ### STEP2: 모든 리스트의 값에 접두어를 추가한다.
# preFix = "LEDTV_"
# for i in range(0, len(tvList2)):
#     # i=3
#     eachModel = tvList2[i]
#     eachModel = preFix + eachModel
#     tvList2[i] = eachModel
# tvList2
# ### 디버깅
# tvList2 = [ 'UN40EN001', 'LEDTV_UN40EN002', 'LEDTV_LEDTV_UN40EN003', 'UN40EN004']
# ### STEP1: 접두어를 선언한다 "LEDTV_"
# ### STEP2: 모든 리스트의 값에 접두어를 추가한다.
# ###        조건1: 접두어가 발견 시 모두 공백처리 하자
# ###              이후 PREFIX 붙이기
# ###        조건1 외에는: 접두어 붙이
# preFix = "LEDTV_"

# for i in range(0, len(tvList2)):
#     # i=0
#     eachModel = tvList2[i]
#     eachModel
#     # 접두어 개수 1개 이상인경우
#     if eachModel.count(preFix) >= 1:
#         eachModel = eachModel.replace(preFix,"")
#         eachModel = preFix + eachModel
#     else:
#         eachModel = preFix + eachModel
#     tvList2[i] = eachModel
# ### 함수
# ### 최소 최대값을 리스트에서 뺀....합을 구하고 싶다
# def trimmedAvg(targetList):
#     """ description: 리스트를 입력값으로 받아서 출력 해줌
#         input: 리스트
#         output: 최소 최대값을 뺀 평균
#     """
#     # targetList = [1,2,5,7,9,10]
#     minValue = min(targetList)
#     maxValue = max(targetList)
#     targetList.remove(minValue)
#     targetList.remove(maxValue)
#     avgList = sum(targetList) / len(targetList)
#     return avgList
# aList = [5,6,7,8,9,10]
# trimmedAvg( aList )

"""### 리스트를 가지고 데이터프레임 생성하기"""

# # Pandas 패키지 불러오기
# import pandas as pd
# from sqlalchemy import create_engine, inspect
# import pandas as pd
# ### 웹 크롤링 시작
# nameList = ["김효관","홍길동","이순신"]
# gubunList = ["200","300","400"]
# resultDf = pd.DataFrame( zip (nameList, gubunList), columns = ["이름","구분"]  )
# ### 웹 크롤링 끝
# resultDf

"""# 2. BeautifulSoup 활용한 태그정보 수집"""

try:
    targetUrl = "https://www.sparkkorea.com/퀴즈"
    resp = requests.get(targetUrl)
    resp.encoding = "utf-8"
    html = resp.text
    print("scaray server connected")
except Exception as e:
    print(e)

# 요청에 대한 응답 값~!!
resp

### bs4 예쁘게 태그별로 추출
bs = bs4.BeautifulSoup(html, "html.parser" )

## div 를 찾아라 근데 속성 class class_spark_quiz
step1Div = bs.find(name="div", attrs={"class":"entry-content"} )
lastDiv = step1Div.find(name="div", attrs={"class":"class_spark_quiz"})
aTags = lastDiv.findAll(name = "a")

linkTextList = []
linkAddressList = []

for i in range(0, len(aTags)):
    # i=0
    eachTag = aTags[i]
    linkText = eachTag.text
    linkAddress = eachTag.attrs["href"]
    linkTextList.append(linkText)
    linkAddressList.append(linkAddress)

resultDf = pd.DataFrame( zip(linkTextList, linkAddressList),
              columns = ["linkname","linkaddress"]  )

resultDf

currentDate = datetime.now()

resultDf["date"] = currentData = currentDate.strftime("%Y_%m%d_%H%M")

resultDf

"""# 3. 데이터 저장 (MySQL)"""

# MySQL 데이터베이스 연결 정보 설정
user = '계정아이디'
password = '계정비번'
host = 'DB접속정보'
port = '3306'
database = 'kopo'

user = 'kopouser'
password = 'kopouser'
host = '13.124.134.168'
port = '3306'
database = 'kopo'

# SQLAlchemy 엔진 생성
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

# 데이터프레임을 MySQL 데이터베이스의 테이블에 저장
### 테이블명 수정 및 저장 시 append"
table_name = 'spark_quiz_data_김효관'
resultDf.to_sql(name=table_name, con=engine, if_exists='append', index=False)
print("database save completed")