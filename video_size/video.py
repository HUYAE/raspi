from flask import Flask, render_template, Response
import cv2
import numpy as np
import dotenv
import os
import sys
from flask_cors import CORS



dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app)
# 영상 파일 경로 지정
VIDEO_PATH = 'http://172.21.3.47:8081/0/stream'

def gen_size_frames():
	# x=520
	# y=7
	# w=962
	# h=853

	# Load image, grayscale, Gaussian blur, Otsu's threshold
	#img = cv2.imread('/var/log/motion/image.jpg')
	img = cv2.imread('image3.png')

	# roi = img[y:y+h, x:x+w]     # roi 지정
	# image = roi.copy()           # roi 배열 복제 ---①

	#image = cv2.subtract(image, -50)
	#image = cv2.add(image, 50)

	# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C | cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 467, 15)
	# edged = cv2.Canny(binary, 0, 200)

	# Find bounding box
	# x,y,w,h = cv2.boundingRect(edged)
	# cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
	# cv2.putText(image, "w={},h={}".format(round(w*2.54/96, 1),round(h*2.54/96, 3)), (x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36,255,12), 2)
	# print(round(h*2.54/96, 3))
	
	ret, buffer = cv2.imencode('.png', img)
	image = buffer.tobytes()
	yield (b'--frame\r\n'
		b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
           

def gen_frames():
	cap = cv2.VideoCapture(VIDEO_PATH)
	while True:
		# 프레임 읽기
		ret, frame = cap.read()

		if not ret:
			break

		# JPEG 인코딩
		ret, buffer = cv2.imencode('.jpg', frame)

		# 스트리밍 데이터 생성
		frame = buffer.tobytes()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

	# 리소스 해제
	cap.release() 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/size_feed')
def size_feed():
	return Response(gen_size_frames(),
					mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
	return Response(gen_frames(),
					mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
