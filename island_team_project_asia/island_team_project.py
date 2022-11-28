# 요기요 크롤링
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re

# url입력
driver = webdriver.Chrome('./chromedriver.exe') # 크롬드라이버 경로 설정
url = "https://www.yogiyo.co.kr/" # 사이트 입력
driver.get(url) # 사이트 오픈
driver.maximize_window() # 전체장
time.sleep(1) # 2초 지연

# 검색창 선택
xpath = '''//*[@id="search"]/div/form/input'''  # 검색창
element = driver.find_element('xpath', xpath)
element.clear()
time.sleep(1)

# 검색창 입력
#value = input("지역을 입력하세요")
element.send_keys("일현로 70")
time.sleep(1)

# 조회버튼 클릭
search_xpath = '''//*[@id="button_search_address"]/button[2]'''
driver.find_element('xpath', search_xpath).click()

time.sleep(1)

# 검색 콤보상자 선택
# 선택 : #search > div > form > ul > li:nth-child(3) > a
search_selector = '//*[@id="search"]/div/form/ul/li[3]/a'
search = driver.find_element('xpath', search_selector)
search.click()
time.sleep(1)


# 조회버튼 클릭
for i in range(3, 14):
    search_xpath = '''//*[@id="category"]/ul/li[{}]/span'''.format(i)
    driver.find_element('xpath', search_xpath).click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # 스크롤을 가장 아래로 내린다

    pre_height = driver.execute_script("return document.body.scrollHeight") # 현재 스크롤 위치 저장

    while True :
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # 스크롤을 가장 아래로 내린다
        time.sleep(2)
        cur_height = driver.execute_script("return document.body.scrollHeight")  # 현재 스크롤을 저장한다.
        if pre_height == cur_height :
            break
        pre_height = cur_height
    time.sleep(1)
time.sleep(1)


# 페이지 소스 출력
html = driver.page_source
html_source = BeautifulSoup(html, 'html.parser')

# 데이터 추출
restaurant_name = html_source.find_all("div", class_ = "restaurant-name ng-binding") #업체명
result_list = []

#데이터 배열
for i in restaurant_name :
    result_list.append(i.string) # 업체명
time.sleep(1)

driver.close() # 크롬드라이버 종료
print(result_list)