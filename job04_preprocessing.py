import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
import pickle

pd.set_option('display.unicode.east_asian_width', True) # 줄 안맞는거 이쁘게 맞춰주기
df = pd.read_csv('./crawling_data/naver_news_titles_20221124.csv')
print(df.head())
print(df.category.value_counts())
df.info()

X = df['titles']
Y = df['category']

encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y)
print(labeled_Y[:5])
print(encoder.classes_)
with open('./models/label_encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)
onehot_Y = to_categorical(labeled_Y)
print(onehot_Y[:5])

okt = Okt() # 형태소 # 뉴스를 형태소 단위로 나눠줄 때 okt를 사용한다.

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)  # stem을 쓰면 동사의 원형으로 만든다. 갔다 -> 가다
    if i % 100 == 0: # 얼마나 됐는지 모르니깐 100개 돌 떄 마다 프린트로 출력
        print('.', end='')
    if i % 10000 == 0:
        print()

stopwords = pd.read_csv('./stopwords.csv', index_col=0)
for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i] not in stopwords['stopword']: # stopwords 안에 없으면 추가해라
                words.append(X[j][i])
    X[j] = ' '.join(words) # 띄어쓰기를 기준으로 하나의 문장으로 이어붙혀 준다.

token = Tokenizer() # 각각의 형태소를 숫자로 라벨링해주는 것
token.fit_on_texts(X) # bow
token_X = token.texts_to_sequences(X)
wordsize = len(token.word_index) + 1 # 제일 긴문장의 길이를 맞춘다.
with open('./models/news_token.pickle', 'wb') as f:
    pickle.dump(token, f)

max_len = 0
for i in range(len(token_X)):
    if max_len < len(token_X[i]):
        max_len = len(token_X[i])
print(max_len)

X_pad = pad_sequences(token_X, max_len) # 앞에다가 0으로 패딩을 입혀서 제일 긴문장의 길이로 맞춘다.

X_train, X_test, Y_train, Y_test = train_test_split(
    X_pad, onehot_Y, test_size=0.1)
print(X_train.shape, Y_train.shape, X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save('./models/news_data_max_{}_wordsize_{}.npy'.format(max_len, wordsize), xy)

