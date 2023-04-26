import multiprocessing as mp
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
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report


def extract_feature(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (64,64))
    feature = LMTRP.LMTRP_process(img) # extract feature from image
    return feature

def train_classifer():
    # Read all the images in custom data-set

    # Read all the images in custom data-set
    path1 = os.path.join(os.getcwd()+"/data1/user/")  # path to images of authorized users
    path2 = os.path.join(os.getcwd()+"/data1/unknown1/")  # path to images of unauthorized users

    num_images = 0
    pool = mp.Pool(mp.cpu_count()) # create a process pool with all available CPUs

    # Store images in a numpy format and corresponding labels in labels list
    features = []
    labels = []

    # For authorized users
    for folder in glob.glob(path1 + '/*'):
        name = folder.split('/')[-1] # get name of the folder
        img_paths = glob.glob(folder + '/*.bmp')
        results = pool.map(extract_feature, img_paths) # extract features for all images in the folder
        features.extend(results)
        num_images += len(img_paths)
        print("Number of images with features extracted:", num_images)
        labels.extend([1] * len(img_paths)) # add the name of the folder as label

    # For unauthorized users
    img_paths = glob.glob(path2 + '/*.bmp')
    results = pool.map(extract_feature, img_paths) # extract features for all images in the folder
    features.extend(results)
    num_images += len(img_paths)
    print("Number of images with features extracted of UNKNOW", num_images)
    labels.extend([-1] * len(img_paths)) # label all images in unknown folder as -1 (false)


    pool.close()
    pool.join()

    features = np.asarray(features)
    labels = np.asarray(labels)
    features = features.reshape(features.shape[0],-1)
    print(features.shape)
    print(labels)
    smote = SMOTE()
    features, labels = smote.fit_resample(features, labels)
    print(features.shape)
    print(labels)
    # Define the parameters for SVM
    param_grid = {'C': [0.1,1, 10, 100, 1000],
                  'gamma': [0.1,0.01,0.001, 0.0001,1],
                  'kernel': ['rbf']}
    # pipe = make_pipeline(SVC(class_weight='balanced'))
    model = GridSearchCV(SVC(class_weight='balanced',probability=True), cv=10,param_grid=param_grid, n_jobs=-1,verbose=3)
    model.fit(features, labels)
    best_params = model.best_params_
    print("Best hyperparameters: ", best_params)

    # Initialize the SVM model with best hyperparameters
    best_svm = SVC(kernel=best_params['kernel'], C=best_params['C'], gamma=best_params['gamma'],probability=True)

    best_svm.fit(features, labels)
    y_pred = best_svm.predict(features)
    print(classification_report(labels, y_pred))


# Save the trained SVM model
    dump(best_svm,"./data1/classifiers/user_classifier.joblib")

    print("Training completed successfully!")

def main():
    mp.freeze_support()
    train_classifer()
if __name__ == '__main__':
    main()
