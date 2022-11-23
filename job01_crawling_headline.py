from bs4 import BeautifulSoup # 헤드라인 뉴스제목만 가지고 왔다.
import requests
import re
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

#url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100' # 정치
#url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101' # 경제
#url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102' # 사회
#url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103' # 문화
#url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104' # 세계
#url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105' # IT

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
df_titles = pd.DataFrame() # requests는 서버에다가 응답을 받는 코드이다.
for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)  # 정치
    resp = requests.get(url, headers=headers) # 뭔가 응답을 받아온다. # 서버에다가 웹페이지를 여는것을 요청하는 것
    # print(list(resp))
    soup = BeautifulSoup(resp.text, 'html.parser')
    # print(soup)
    title_tags = soup.select('.cluster_text_headline') # . 붙이면 class # 리스트를 만들어준 것
    print(title_tags[0].text) # 제목만 뽑고 싶으면 [0].text를 쓰면 된다.
    titles = []
    for title_tag in title_tags:
        titles.append(title_tag.text)
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i] # 다 돌고나면 df_titles에 모든 카테고리가 들어간다.
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)
print(df_titles)
print(df_titles.category.value_counts())
df_titles.to_csv('./crawlind_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False) # 마지막에 날짜 넣은 함수
# index 안보이게 하기 위해서 index=False를 주었다.