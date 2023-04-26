import numpy as np
import os, cv2
import LMTRP
from sklearn.svm import SVC
from joblib import dump ,load
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
import joblib
import glob

def train_classifer():
    # Read all the images in custom data-set

# Read all the images in custom data-set
    path1 = os.path.join(os.getcwd()+"/data/user/")  # path to images of authorized users
    path2 = os.path.join(os.getcwd()+"/data/unknown1/")  # path to images of unauthorized users

    features = []
    labels = []
    num_images = 0

    # Store images in a numpy format and corresponding labels in labels list
    for folder in glob.glob(path1 + '/*'):
        name = folder.split('/')[-1] # get name of the folder
        for imgpath in glob.glob(folder + '/*.bmp'):
            img = cv2.imread(imgpath)
            img = cv2.resize(img, (64,64))
            feature = LMTRP.LMTRP_process(img) # extract feature from image
            features.append(feature)
            num_images += 1
            print("Number of images with features extracted:", num_images)
            labels.append(1) # add the name of the folder as label

    for imgpath in glob.glob(path2 + '/*.bmp'):
        img = cv2.imread(imgpath)
        img = cv2.resize(img, (64,64))
        feature = LMTRP.LMTRP_process(img) # extract feature from image
        features.append(feature)
        num_images += 1
        print("Number of images with features extracted of UNKNOW", num_images)
        labels.append(-1) # label all images in unknown folder as -1 (false)

    features = np.asarray(features)
    labels = np.asarray(labels)
    features = features.reshape(features.shape[0],-1)
    # print(features.shape)
    # print(labels)
    # Define the parameters for SVM
    

    param_grid = {'svc__C': [1, 10, 100, 1000],
              'svc__gamma': [0.1,0.01,0.001, 0.0001,1],
              'svc__kernel': ['rbf']}
    pipe = make_pipeline(SVC())
    model = GridSearchCV(pipe, cv=10,param_grid=param_grid, n_jobs=-1,verbose=3)
    model.fit(features, labels)
    best_params = model.best_params_
    print("Best hyperparameters: ", best_params)

    # Initialize the SVM model with best hyperparameters
    best_svm = SVC(kernel=best_params['svc__kernel'], C=best_params['svc__C'], gamma=best_params['svc__gamma'])

    best_svm.fit(features, labels)

# Save the trained SVM model
    dump(best_svm,"./data/classifiers/user_classifier.joblib")

    print("Training completed successfully!")

def predict(image_path, threshold=0.5):
    # Load the trained SVM model
    svm_model = joblib.load('./data/classifiers/user_classifier.joblib')
    img=cv2.imread(image_path)
    # Extract features from the input image
    img = cv2.resize(img, (64, 64))
    feature = LMTRP.LMTRP_process(img)
    
    feature = feature.reshape(1, -1)
    x=svm_model.predict(feature)
    # Predict the label of the input image and get the decision function value
    decision = svm_model.decision_function(feature)

    # Calculate the confidence level of the prediction
    confidence = 1 / (1 + np.exp(-decision))
    print(confidence)
    # Check if the predicted label is 1 (true) or -1 (false) based on the threshold
    if x==1:
        print("Access granted!")
    else:
        print("Access denied.")

# train_classifer()
# predict('./random/han.bmp')