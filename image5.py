import cv2
import numpy as np

background_img = cv2.imread('background.jpg')
object_img = cv2.imread('object.jpg')

background_img = cv2.resize(background_img, (object_img.shape[1], object_img.shape[0]))

# 두 이미지의 차이를 계산
diff = cv2.absdiff(background_img, object_img)

# 차이 이미지를 그레이스케일로 변환
gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
object_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C | cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 467,20)

cv2.imshow("object_img", object_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
