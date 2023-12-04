import cv2

webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

num= 0  

while webcam.isOpened():
    status, frame = webcam.read()

    if status:
        cv2.imshow("video", frame)
    if num == 0:
        cv2.imwrite('image4.jpg', frame)
        num = 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
