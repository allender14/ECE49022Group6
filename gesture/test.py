import cv2

# Function to read frames from the shared video stream
def read_video_stream(cap):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Process the frame here, you can add your own logic
        # For example, displaying the frame in a window
        cv2.imshow('Shared Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to do other processing with the shared video stream
def process_video_stream(cap):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Add your processing logic here
        # For example, you can perform some image processing on the frame

# Create a VideoCapture object for the shared video stream
cam_port = 0
video_stream = cv2.VideoCapture(cam_port)  # Replace with your video source

# Create and start two threads for the functions
import threading
read_thread = threading.Thread(target=read_video_stream, args=(video_stream,))
process_thread = threading.Thread(target=process_video_stream, args=(video_stream,))

read_thread.start()
process_thread.start()

# Wait for both threads to finish
read_thread.join()
process_thread.join()

# Release the video stream when done
video_stream.release()

