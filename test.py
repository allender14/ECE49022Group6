import cv2
import time
import subprocess

cap = cv2.VideoCapture(0)

start_time = time.time()
while cap.isOpened():
    ret, frame = cap.read()
    print(time.time() - start_time)
    if not ret:
        break

    if cv2.waitKey(1) == 27:
        break

    if (time.time() - start_time) > 5:
        cv2.destroyAllWindows()
        subprocess.run(["python", "./src/gesture_recognition.py"])
        start_time = time.time()

    cv2.imshow("window1", frame)

cap.release()
cv2.destroyAllWindows()

