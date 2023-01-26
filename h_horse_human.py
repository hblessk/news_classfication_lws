import numpy as np
from keras.models import Sequential
from keras.layers import *
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

X_train, X_test, Y_train, Y_test = np.load('./horse_human/binary_image_data_h.npy', allow_pickle=True)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), padding='same',
                 input_shape=(64, 64, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(32, kernel_size=(3, 3), padding='same',
                 activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(32, kernel_size=(3, 3), padding='same',
                 activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.summary()
# 모델의 학습을 어떻게 할지 미리 설정해 놓은 것
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['binary_accuracy'])
early_stopping = EarlyStopping(monitor='val_binary_accuracy', patience=7)
fit_his = model.fit(X_train, Y_train, batch_size=32, epochs=10,
                    validation_split=0.15, callbacks=[early_stopping])
score = model.evaluate(X_test, Y_test)
print('Evaluation loss:', score[0])
print('Evaluation accuracy:', score[1])
model.save('./horse_humans_{}.h5'.format(str(np.around(score[1], 2))[-2:]))
plt.plot(fit_his.history['binary_accuracy'], label='binary_accuracy')
plt.plot(fit_his.history['val_binary_accuracy'], label='val_binary_accuracy')
plt.legend()
plt.show()
plt.plot(fit_his.history['loss'], label='loss')
plt.plot(fit_his.history['val_loss'], label='val_loss')
plt.legend()
plt.show()