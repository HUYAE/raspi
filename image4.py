#import cv2

#img = cv2.imread("object.jpg") # Read image

#t_lower = 150 # Lower Threshold
#t_upper = 200 # Upper threshold
#aperture_size = 5 # Aperture size
#L2Gradient = True # Boolean

# Applying the Canny Edge filter with L2Gradient = True
#edge = cv2.Canny(img, t_lower, t_upper, L2gradient = L2Gradient )

#cv2.imshow('original', img)
#cv2.imshow('edge', edge)
#cv2.waitKey(0)
#cv2.destroyAllWindows()




import cv2

src = cv2.imread("object2.jpg")
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C | cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 467,20)

cv2.imshow("gray", gray)
cv2.imshow("binary", binary)
cv2.waitKey(0)
cv2.destroyAllWindows()
