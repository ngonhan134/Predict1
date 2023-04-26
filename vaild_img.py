import cv2
import numpy    as np
import cv2
import numpy as np
import LMTRP
def is_valid_ROI(image):
    # Convert image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Calculate histogram of saturation channel
    s = cv2.calcHist([hsv], [1], None, [256], [0, 256])

    # Calculate percentage of pixels with saturation >= p
    p = 0.05
    s_perc = np.sum(s[int(p * 255):-1]) / np.prod(hsv.shape[0:2])

    # Percentage threshold; above: valid image, below: noise
    s_thr = 0.5
    return s_perc > s_thr

# Load image and check if it is valid
image_path = './random/RGB.bmp'
image = cv2.imread(image_path)
print("Feature of RBG : ")
print(LMTRP.LMTRP_process(image))
feature = LMTRP.LMTRP_process(image).reshape(1, -1)
print("Feature of Shape RGB =  ",feature)
# lab= cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
# gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# cv2.imshow("gray",gray)
# cv2.imwrite("test1.bmp",gray)
# hsv = cv2.cvtColor(gray, cv2.COLOR_BGR2HSV)

# cv2.imshow("HSV",lab)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
print(is_valid_ROI(image))

image_path1 = './random/Nhan_Gray.bmp'
image1 = cv2.imread(image_path1)
print("Feature of Gray : ")
print(LMTRP.LMTRP_process(image1))
print("Feature of Shape Gray =  ",LMTRP.LMTRP_process(image1).shape)
# import train_with_multi
# import multiprocessing as mp

# if __name__ == '__main__':
#     mp.freeze_support()
#     train_with_multi.main()
