from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
pages = [101, 101, 101, 71, 94, 73] # 중복데이터를 늘리던, 많은 것을 줄인다.
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101#&date=%2000:00:00&page=2'

options = webdriver.ChromeOptions()
#options.add_argument('headless') # 이 옵션을 주면 브라우저를 안보여준다. 띄어지지만 안보임
options.add_argument('lang=kr_KR')
driver = webdriver.Chrome('./chromedriver', options=options)
df_title = pd.DataFrame()
for i in range(0, 6): # section
    titles = []
    for j in range(1, 11): # 페이지수 여기서 -1이라 위에 +1 해줌 # page
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i, j)
        driver.get(url)
        time.sleep(0.2)
        for k in range(1, 5): # x_path
            for l in range(1, 6): # x_path
                x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k, l) # 이렇게 하면 4*5해서 20개 긁어옴
                try:
                    title = driver.find_element('xpath', x_path).text
                    title = re.compile('[^가-힣 ]').sub(' ', title)
                    titles.append(title)

                except NoSuchElementException as e: # except는 에러
                    x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k, l)
                    title = driver.find_element('xpath', x_path).text
                    title = re.compile('[^가-힣 ]').sub(' ', title)
                    titles.append(title)
                except:
                    print('error', i, j, k, l)

        if j % 10 == 0:
            df_section_title = pd.DataFrame(titles, columns=['titles'])
            df_section_title['category'] = category[i]
            df_title = pd.concat([df_title, df_section_title], ignore_index=True)
            df_title.to_csv('./crawling_data/crawling_data_{}_{}.csv'.format(category[i], j), index=False)
            titles = []