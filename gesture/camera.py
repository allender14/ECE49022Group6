import cv2

def camera(cam):

    while True:
        ret, frame = cam.read()

        if not ret:
            # Error reading frame from the camera
            break

        try:
          cv2.imshow("Live Stream", frame)

          # Press 'q' to exit the loop and close the window
          if cv2.waitKey(1) & 0xFF == ord('w'):
              break

        except cv2.error:
          pass

    cam.release()
    cv2.destroyWindow("Live Stream")

if __name__ == "__main__":
  cam_port = 0
  cam = cv2.VideoCapture(cam_port)
  camera(cam)
