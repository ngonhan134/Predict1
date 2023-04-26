from ROI_Gray import *
import os
import LMTRP
import joblib
import numpy as np
import cv2
import glob
from PIL import Image 


def check():
# đường dẫn tới thư mục chứa các ảnh
    path_out_img = './ROI1'
    # Xóa toàn bộ tệp tin ảnh trong thư mục path_out_img

    file_list = glob.glob(os.path.join(path_out_img, '*.bmp'))
    for file_path in file_list:
        os.remove(file_path)


    roiImageFromHand(path_out_img, option=2, cap=cv2.VideoCapture(0))


    # lọc ra danh sách các ảnh trong folder
    image_list = glob.glob(os.path.join(path_out_img, '*.bmp'))

    # load mô hình đã được train
    recognizer = joblib.load('./data1/classifiers/user_classifier.joblib')
    pred = 0
    print_flag = True

    results = []
    confidence_scores = []
    for img in image_list:
        img= cv2.imread(img)
   
        img = cv2.resize(img, (64, 64))
   
        feature = LMTRP.LMTRP_process(img)
        
        # feature = LMTRP.LMTRP_process(img)
        feature = feature.reshape(1, -1)
        decision = recognizer.decision_function(feature)
        confidence = 1 / (1 + np.exp(-decision))
        predict = recognizer.predict_proba(feature)
        
        # print(confidence)
        # print(predict)


        unknown_prob = predict[0][0]
        user_prob = predict[0][1]

        if user_prob > 0.7:
            pred = pred + 1
            confidence_scores.append(confidence)
        if print_flag:
            print("Prediction............!")
            print_flag = False
    sum=np.sum(confidence_scores)

    if pred>=5 and sum>=3: 
        print(np.sum(confidence_scores))
        print(pred)
        print('Nhan')
        return True
    else:
        print(np.sum(confidence_scores))
        print(pred)
        print('unknown')
        return False


# import glob
# import os
# import cv2
# import numpy as np
# import joblib
# from concurrent.futures import ThreadPoolExecutor
# from concurrent.futures import ProcessPoolExecutor
# from ROI_Gray import *
# import os
# import LMTRP
# import joblib
# import numpy as np
# import cv2
# import glob
# from PIL import Image 

# def process_image(img_path):
#     recognizer = joblib.load('./data1/classifiers/user_classifier.joblib')
#     img = cv2.imread(img_path)
#     img = cv2.resize(img, (64, 64))
#     feature = LMTRP.LMTRP_process(img)
#     feature = feature.reshape(1, -1)
#     decision = recognizer.decision_function(feature)
#     confidence = 1 / (1 + np.exp(-decision))
#     predict = recognizer.predict_proba(feature)
#     unknown_prob = predict[0][0]
#     user_prob = predict[0][1]

#     return user_prob, confidence

# def check():
#     path_out_img = './ROI1'
#     file_list = glob.glob(os.path.join(path_out_img, '*.bmp'))
#     for file_path in file_list:
#         os.remove(file_path)

#     roiImageFromHand(path_out_img, option=2, cap=cv2.VideoCapture(0))
#     image_list = glob.glob(os.path.join(path_out_img, '*.bmp'))
#     recognizer = joblib.load('./data1/classifiers/user_classifier.joblib')
#     pred = 0
#     confidence_scores = []
#     max_workers = 4
#     with ProcessPoolExecutor(max_workers=max_workers) as executor:
#         results = list(executor.map(lambda img_path: process_image(img_path), image_list))

#     for user_prob, confidence in results:
#         if user_prob > 0.7:
#             pred = pred + 1
#             confidence_scores.append(confidence)

#     sum_confidence = np.sum(confidence_scores)
   
#     if pred >= 5 and sum_confidence >= 3: 
#         print(sum_confidence)
#         print(pred)
#         print('Nhan')
#         return True
#     else:
#         print(sum_confidence)
#         print(pred)
#         print('unknown')
#         return False

# check()