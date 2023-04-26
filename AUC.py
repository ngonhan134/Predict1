import os
import numpy as np
import cv2
import LMTRP
import ROI
from tqdm import tqdm
from sklearn.model_selection import GridSearchCV
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import pickle
from sklearn.metrics import classification_report, confusion_matrix
path = 'DATA_RGB/'

labels = os.listdir(path)

print("Tổng số file trong DATA_SET: ", len(labels))

X = []
y = []
for i, label in enumerate(labels):
    img_filenames = os.listdir('{}{}/'.format(path, label))
    for filename in tqdm(img_filenames, desc='Processing ' + label):
        filepath = '{}{}/{}'.format(path, label, filename)
        img = cv2.imread(filepath)
        img = cv2.resize(img, (64, 64))
        
        # Ignore if not found face in image
        try:
            encode = LMTRP.LMTRP_process(img)
        except Exception as e:
            print(e, ":", label, filename)
            continue
        
        X.append(encode)
        y.append(i)

X = np.asarray(X)
y = np.asarray(y)

# # Tạo DataFrame từ mảng X và thêm cột nhãn y
# df = pd.DataFrame(X.reshape(X.shape[0], -1))
# df = df.assign(label=y)
# df.to_csv('feature_rgb32.csv')
# data = pd.read_csv('data1.csv',index_col=0)

# # # # Hiển thị 5 dòng đầu tiên của DataFrame
# # print(data.head())

# X = data.iloc[:, :-1].values
# y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=42)


X_test = X_test.reshape(X_test.shape[0], -1)
X_train = X_train.reshape(X_train.shape[0], -1)


print(X_train.shape, X_test.shape)
print(y_train.shape, y_test.shape)
# param_grid = {'C': [1, 10, 100, 1000,10000],
#               'gamma': [0.1,0.01,0.001, 0.0001,0.00001],
#               'kernel': ['rbf','linear','sigmoid']}
param_grid = {'C': np.logspace(3, 5, num=20, dtype=float),
              'gamma': np.logspace(-4, -1, num=20, dtype=float),
              'kernel': ['rbf']
              }
svc_model = svm.SVC()

grid_search = GridSearchCV(svc_model, param_grid, cv=2,verbose=3)
grid_search.fit(X_train, y_train)


print("Best parameters: ", grid_search.best_params_)
print("Best accuracy: ", grid_search.best_score_)
print(f'Train - :{grid_search.score(X_train,y_train):3f}')
print(f'Test - :{grid_search.score(X_test,y_test):3f}')

# Sử dụng bộ tham số tối ưu để huấn luyện mô hình trên toàn bộ tập huấn luyện
svc_model = svm.SVC(kernel=grid_search.best_params_['kernel'],
                     C=grid_search.best_params_['C'],
                     gamma=grid_search.best_params_['gamma'])

# Train Accuracy
svc_model.fit(X_train, y_train)

pred = svc_model.predict(X_train)
train_acc = accuracy_score(y_train, pred)
print("Training Accuracy: ", train_acc)

## Test Accuracy
pred = svc_model.predict(X_test)
test_acc = accuracy_score(y_test, pred)
print("Test Accuracy: ", test_acc)
# Tính toán và in ra báo cáo đánh giá mô hình
print(classification_report(y_test, pred))

model_name = 'svm-{}.model'.format(str(int(test_acc*100)))
pickle.dump(svc_model, open(model_name, 'wb'))
