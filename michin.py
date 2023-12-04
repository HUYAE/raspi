import cv2
import numpy as np
import dotenv
import os
import sys

dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_path)

x=520
y=7
w=962
h=853

# Load image, grayscale, Gaussian blur, Otsu's threshold
img = cv2.imread('/var/log/motion/image.jpg')

roi = img[y:y+h, x:x+w]     # roi 지정
image = roi.copy()           # roi 배열 복제 ---①

#image = cv2.subtract(image, -50)
#image = cv2.add(image, 50)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C | cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 467,15)
cv2.imshow("binary", binary)
edged = cv2.Canny(binary, 100, 500)

# Find bounding box
x,y,w,h = cv2.boundingRect(edged)
cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
cv2.putText(image, "w={},h={}".format(round(w*2.54/96, 1),round(h*2.54/96, 3)), (x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36,255,12), 2)
print(round(h*2.54/96, 3))

# cv2.imshow("thresh", thresh)
cv2.imshow("image", image)
cv2.imshow("edged", edged)
cv2.waitKey()
