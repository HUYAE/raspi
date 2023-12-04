import cv2
import numpy as np

# 이미지 읽어오기
img = cv2.imread('image4.jpg')

# 초기 마스크 생성
mask = np.zeros(img.shape[:2], np.uint8)

# 관심 있는 부분(ROI) 지정
roi = (100, 100, 300, 300)
cv2.rectangle(mask, (roi[0], roi[1]), (roi[0]+roi[2], roi[1]+roi[3]), (255, 255, 255), -1)

# GrabCut 알고리즘 적용
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
mask, bgdModel, fgdModel = cv2.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

# 추출된 부분을 표시하는 마스크 생성
mask_fg = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')

# 추출된 부분의 윤곽선 검출
contours, hierarchy = cv2.findContours(mask_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 길이가 가장 긴 윤곽선 추출
longest_contour = max(contours, key=cv2.contourArea)

# 윤곽선 그리기
cv2.drawContours(img, [longest_contour], -1, (0, 255, 0), 2)

# 최소한의 직사각형 구하기
rect = cv2.minAreaRect(longest_contour)
box = cv2.boxPoints(rect)
box = box.astype(int)

# 사각형 그리기
cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

# 길이 표시
perimeter = cv2.arcLength(longest_contour, True)
text = f"Length: {perimeter:.2f}"
cv2.putText(img, text, (int(rect[0][0]), int(rect[0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# 이미지 출력
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
