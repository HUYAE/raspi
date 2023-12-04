import cv2

g_l_threhold = (30, 80, 80)
g_h_threhold = (150, 255, 255)

img = cv2.imread('object2.jpg')

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('hsv_img', hsv_img)	
g_mask = cv2.inRange(hsv_img, g_l_threhold, g_h_threhold)
green_img = cv2.bitwise_and(img, img, mask=g_mask)          

cv2.imshow('IMG',img)
cv2.imshow('GREEN', green_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
