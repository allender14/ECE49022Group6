import cv2
import threading
from capture import photo_capture
from camera import camera

cam_port = 0
cam = cv2.VideoCapture(cam_port)

# Create the Live Stream window before calling functions
cv2.namedWindow("Live Stream", cv2.WINDOW_NORMAL)

# Start the camera feed in a separate thread
camera_thread = threading.Thread(target=camera, args=(cam,))
camera_thread.start()

# Run the photo capture function
photo_capture(cam)

# Wait for the camera thread to finish
camera_thread.join()

cv2.destroyAllWindows()  # Close all OpenCV windows
cam.release()

