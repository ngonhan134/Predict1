import joblib
import cv2
import LMTRP
import numpy as np

# Load classifier
clf = joblib.load("./data/classifiers/nhan_classifier.joblib")

# Load image and extract feature
img = cv2.imread("./random/du.bmp")
print(img.shape)
feature = LMTRP.LMTRP_process(img)
feature = feature.flatten()
print(feature)
# Predict
prediction = clf.predict([feature])

# Apply threshold
if prediction[0] == 1:
    print("The new image belongs to the data set.")
else:
    print("The new image does not belong to the data set.")
