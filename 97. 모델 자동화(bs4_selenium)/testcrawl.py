# -*- coding: utf-8 -*-
import time
from selenium.webdriver.support.ui import Select
from sqlalchemy import create_engine, inspect

# Selenium과 webdriver-manager를 사용한 Chrome 브라우저 실행 코드
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import bs4
import time
# WebDriver 설치 및 브라우저 실행 설정
options = webdriver.ChromeOptions()

options.add_argument("--headless")  # 헤드리스 모드로 실행 (브라우저 창을 표시하지 않음)
options.add_argument("window-size=1920x1080") # 헤드리스 모드로 실행 (명시적으로 표기)
options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화 (가상 환경에서 안정적인 실행을 위해)
options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 비활성화 (메모리 부족 방지)
# user-agent 값 설정
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")


service = Service(executable_path="/home/ubuntu/pywork/chromedriver-linux64/chromedriver")
# WebDriver로 Chrome 브라우저 실행

driver = webdriver.Chrome(service=service, options=options)

# 웹페이지 파싱 될때까지 최대 3초 기다림
driver.implicitly_wait(3)

#driver.get("https://www.google.com")

schoolInfo = "https://www.schoolinfo.go.kr/"
# 학교 알리미 사이트로 이동
driver.get(schoolInfo)
searchInputText = '//*[@id="SEARCH_KEYWORD"]'
searchInputEl = driver.find_element(By.XPATH, searchInputText)
keyword = "초등학교"
searchInputEl.send_keys(keyword)
time.sleep(3)

serchBtn = '//*[@id="headerSearchForm"]/button'
searchBtnEl = driver.find_element(By.XPATH, serchBtn)
searchBtnEl.click()
time.sleep(3)

driver.save_screenshot("here.jpg")

# ### 셀렉트 박스
# selectGubun1 = '//*[@id="FNDN_SC_CD"]'
# selectGubun1El = driver.find_element(By.XPATH, selectGubun1)
# selectGubun1El.click()

# 셀렉트 박스 요소 찾기
select_box = driver.find_element(By.XPATH, '//*[@id="FNDN_SC_CD"]')
# Select 객체를 사용하여 셀렉트 박스 제어
select = Select(select_box)
# "뉴스" 옵션 선택 (옵션 값 혹은 텍스트를 통해 선택할 수 있습니다)
select.select_by_index(0)

selectGubun2 = '//*[@id="SIDO_CODE"]'
# 셀렉트 박스 요소 찾기
select_box = driver.find_element(By.XPATH,selectGubun2)

# Select 객체를 사용하여 셀렉트 박스 제어
select = Select(select_box)
# "뉴스" 옵션 선택 (옵션 값 혹은 텍스트를 통해 선택할 수 있습니다)
select.select_by_index(1)

selectGubun3 = '//*[@id="GUGUN_CODE"]'
# 셀렉트 박스 요소 찾기
select_box = driver.find_element(By.XPATH,selectGubun3)
# Select 객체를 사용하여 셀렉트 박스 제어
select = Select(select_box)
# "뉴스" 옵션 선택 (옵션 값 혹은 텍스트를 통해 선택할 수 있습니다)
select.select_by_visible_text("송파구")
driver.save_screenshot("here.jpg")
### 검색 버튼 클릭
searchBtn = '//*[@id="contents"]/div/div[1]/div/a'
searchBtnEl = driver.find_element(By.XPATH, searchBtn)
searchBtnEl.click()

time.sleep(2)
# 더보기 버튼 클릭
addxPath = '//*[@id="contents"]/div/div[2]/a'
driver.find_element(By.XPATH, addxPath).click()
time.sleep(2)

driver.save_screenshot("here.jpg")

schoolName = []
totalNumber = []
for page in range(0, 9):
    html = driver.page_source
    bsObj = bs4.BeautifulSoup(html,"html.parser")
    import re
    divs = bsObj.findAll('div', attrs={"class":"basic_data"})

    for i in range(0, len(divs)):
        sName = divs[i].find(name="a").text
        schoolName.append( sName )

        indata = divs[i].findAll(name="div", attrs={"class":"l_box"})[1].find(name="span",attrs={"class":"md"}).text
        # 줄 단위로 나눈 후 공백 제거
        lines = indata.split()

        # '745명'이 있는 부분 찾기
        for part in lines:
            if '명' in part:
                # '명'을 제거하여 숫자만 추출
                total_students = part.replace('명', '')
                # print(total_students)
                totalNumber.append(total_students)
                break
    # 다음 페이지 버튼 클릭
    nextBtn = '//*[@id="contents"]/div/div[3]/div[1]/a[12]'

    driver.find_element(By.XPATH, nextBtn).click()
    time.sleep(3)

import pandas as pd

df2 = pd.DataFrame( zip(schoolName, totalNumber), columns=["학교명","인원"] )

df2["인원"] = df2.인원.str.replace(",","")

df2["인원"] = df2["인원"].astype(int)

df2["인원"].sum()

df2.sort_values(by=["인원"], ascending=False).reset_index()

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
table_name = 'spark_selenium_data_김효관'
df2.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
print("database save completed")
