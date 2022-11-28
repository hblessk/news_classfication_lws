import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import *


X_train, X_test, Y_train, Y_test = np.load(
    './models/news_data_max_20_wordsize_11881.npy', allow_pickle=True)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

model = Sequential() # 형태소들이 계산할 수 있는 상태가 됌
model.add(Embedding(11881, 300, input_length=20)) # 의미 없는 숫자를 의미있는 문자로 바꿔주는 행동
model.add(Conv1D(32, kernel_size=5, padding='same', activation='relu')) # 한줄짜리니 kernel 5줌
model.add(MaxPool1D(pool_size=1)) # 1써주면 아무일 생기지 않지만 습관적으로 써준다.
model.add(GRU(128, activation='tanh', return_sequences=True)) # 단어에 순서가 있기에 GRU를 사용하면 좋다.
model.add(Dropout(0.3))
model.add(GRU(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(GRU(64, activation='tanh'))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(6, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=128, epochs=10,
                     validation_data=(X_test, Y_test))
model.save('./models/news_category_classfication_model_{}.h5'.format(
    np.round(fit_hist.history['val_accuracy'][-1], 3)))
plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.plot(fit_hist.history['val_accuracy'], label='val_accuracy')
plt.legend()
plt.show()
