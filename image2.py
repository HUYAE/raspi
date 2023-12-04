import cv2

# 바탕 이미지와 물체가 있는 이미지 불러오기
background_img = cv2.imread('back.jpg')
object_img = cv2.imread('object2.jpg')

# 두 이미지의 차이 계산
diff_img = cv2.absdiff(background_img, object_img)
cv2.imshow('diff_img', diff_img)
# 차이 이미지를 grayscale로 변환
gray_img = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray_img', gray_img)
# threshold 값 설정
threshold = 25

# threshold 값 이상인 픽셀을 255로, 나머지 픽셀을 0으로 이진화
_, thresh_img = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY)

# 배경을 흰색으로 바꾸기
thresh_img[thresh_img != 0] = 255

# 이미지 출력
cv2.imshow('thresh_img', thresh_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
