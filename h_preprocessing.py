from PIL import Image   # pillow
import glob
import numpy as np
from sklearn.model_selection import train_test_split
import os
import shutil
import time


def read_all_file(path):
    output = os.listdir(path)
    file_list = []

    for i in output:
        if os.path.isdir(path + "/" + i):
            file_list.extend(read_all_file(path + "/" + i))
        elif os.path.isfile(path + "/" + i):
            file_list.append(path + "/" + i)

    return file_list


def copy_all_file(file_list, new_path):
    for src_path in file_list:
        file = src_path.split("/")[-1]
        shutil.copyfile(src_path, new_path + "/" + file)
        print("파일 {} 작업 완료".format(file))  # 작업한 파일명 출력


start_time = time.time()  # 작업 시작 시간

src_path = "./horse_human/"  # 기존 폴더 경로
new_path = "./horse_human/add_h/"  # 옮길 폴더 경로

file_list = read_all_file(src_path)
copy_all_file(file_list, new_path)


img_dir = './horse_human/add_h/'
categories = ['horse', 'human']
image_w = 64
image_h = 64
pixel = image_h * image_w * 3
X = []
Y = []
files = None
for idx, category in enumerate(categories):
    files = glob.glob(img_dir + category + '*.png') # 모든 경로의 jpg파일
    print(category, len(files))
    for i, f in enumerate(files):
        try:
            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((image_w, image_h))
            data = np.asarray(img)
            X.append(data)
            Y.append(idx)
            if i % 1 == 0:
                print(category, ':', f)
        except:
            print('error', f)
X = np.array(X)
Y = np.array(Y)
X = X / 255
#print(X[0])
#print(Y[0])
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1)
xy = (X_train, X_test, Y_train, Y_test)
np.save('./horse_human/binary_image_data_h.npy', xy)


