import cv2
import numpy as np
import dotenv
import os
import sys

dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_path)

def size() :
	# x=int(os.environ['X'])
	# y=int(os.environ['Y'])
	# w=int(os.environ['W'])
	# h=int(os.environ['H'])
	
	x=563
	y=97
	w=792
	h=877

	# Load image, grayscale, Gaussian blur, Otsu's threshold
	img = cv2.imread('/var/log/motion/image.jpg')

	roi = img[y:y+h, x:x+w]     # roi 지정
	image = roi.copy()           # roi 배열 복제 ---①

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 0, 200)

	# Find bounding box
	x,y,w,h = cv2.boundingRect(edged)
	cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
	#cv2.putText(image, "w={},h={}".format(round(w*2.54/96, 1),round(h*2.54/96, 3)), (x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36,255,12), 2)
	print(round(h*2.54/96, 3))

	# cv2.imshow("thresh", thresh)
	#cv2.imshow("image", image)
	#cv2.imshow("edged", edged)
	#cv2.waitKey()

	
	return round(h*2.54/96, 1)

size()
