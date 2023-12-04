import cv2
import numpy as np

background_img = cv2.imread('back.jpg')
object_img = cv2.imread('plant.jpg')

background_img = cv2.resize(background_img, (object_img.shape[1], object_img.shape[0]))
cv2.imshow('background_img', background_img)

# 두 이미지의 차이를 계산
diff = cv2.absdiff(background_img, object_img)
cv2.imshow('diff', diff)

# 차이 이미지를 그레이스케일로 변환
gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray_diff', gray_diff)

# 이진화
_, threshold = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    if cv2.contourArea(contour) > 7000:  # 노이즈 제거를 위해 면적이 일정 이상인 경우에만 실행
        cv2.rectangle(object_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow('object_img', object_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
