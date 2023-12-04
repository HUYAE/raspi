import cv2
import time

video_file_path = 'plant.avi'
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # 가로
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # 세로
# 코덱 설정 및 파일 이름 지정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('plant.avi', fourcc, 30.0, (1920, 1080))
while True:
    ret, frame = cap.read()
    if not ret:
        break

    out.write(frame)  # 영상 저장
    print(time.time() % 5)
    print(out)
    # 5초마다 파일 덮어쓰기
    if time.time() % 5 == 0:
        out.release()
        out = cv2.VideoWriter('plant.avi', fourcc, 30.0, (1920, 1080))

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
