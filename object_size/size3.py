import cv2
import numpy as np
# Load image, grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread("image5.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# GrabCut 알고리즘 적용
kernel = np.ones((3,3),np.uint8)
erosion = cv2.erode(thresh, kernel, iterations=3)
dilation = cv2.dilate(erosion, kernel, iterations=3)
mask = dilation.copy()
mask[mask != 0] = cv2.GC_PR_FGD

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
rect = (10, 10, image.shape[1]-20, image.shape[0]-20)
mask, bgdModel, fgdModel = cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)
mask = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')

# 마스킹된 이미지 추출
masked_img = cv2.bitwise_and(image, image, mask=mask)

gray_mask = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
ret, thresh_mask = cv2.threshold(gray_mask, 0, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 가장 큰 윤곽선 검출
max_contour = max(contours, key=cv2.contourArea)

# 윤곽선 근사화
epsilon = 0.01 * cv2.arcLength(max_contour, True)
approx = cv2.approxPolyDP(max_contour, epsilon, True)

# 길이 측정
length = cv2.arcLength(approx, True)

# 길이 표시
cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
cv2.putText(image, "Length: {:.2f} pixels".format(length), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# 결과 출력
cv2.imshow("Masked Image", masked_img)
cv2.imshow("Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Find bounding box
x,y,w,h = cv2.boundingRect(thresh)
cv2.rectangle(masked_img, (x, y), (x + w, y + h), (36,255,12), 2)
cv2.putText(masked_img, "w={},h={}".format(round(w*2.54/72, 1),round(h*2.54/72, 1)), (x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36,255,12), 2)

cv2.imshow("thresh", thresh)
cv2.imshow("image", masked_img)
cv2.waitKey()
