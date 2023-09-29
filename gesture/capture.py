import cv2
import time
import datetime


def streaming(cam):
  cv2.namedWindow("Photo Capture", cv2.WINDOW_NORMAL)

  flag = False
  start = 0
  detected = True
  while True:
    result, frame = cam.read()
    cv2.imshow("Photo Capture", frame)

    if not result:
        break

    flag, start = photo_capture(frame, flag, start)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  cam.release()
  cv2.destroyWindow("Photo Capture")

def photo_capture(frame, flag = True, start = 0, detected = True):
  #if cv2.waitKey(1) & 0xFF == ord('t'):
  if detected:
    print("count down starts")
    flag = True
    start = time.time()

  if flag and (time.time() - start >= 5):
    current_time = datetime.datetime.now()
    cv2.imwrite(f"./photo/{current_time}.png", frame)
    print(f"Photo path ./photo/{current_time}.png")
    flag = False

  if flag:
    print(time.time() - start)

  return flag, start

if __name__ == "__main__":
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    streaming(cam)

