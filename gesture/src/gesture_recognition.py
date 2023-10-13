import argparse
import sys
import time
import datetime

import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import BaseOptions, vision
from mediapipe.framework.formats import landmark_pb2
from capture import photo_capture

COUNTER, FPS = 0, 0
START_TIME = time.time()

def run(model: str, num_hands: int,
        min_hand_detection_confidence: float,
        min_hand_presence_confidence: float,
        min_tracking_confidence: float,
        camera_id: int, width: int, height: int) -> None:

  cap = cv2.VideoCapture(0)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  row_size = 50
  left_margin = 24
  text_color = (0,0,0)
  font_size = 1
  font_thickness = 1
  fps_avg_frame_count = 10

  label_text_color = (0, 0, 0)
  label_background_color = (255, 255, 255)
  label_font_size = 1
  label_thickness = 2
  label_padding_width = 100

  recognition_frame = None
  recognition_result_list = []

  def save_result(result: vision.GestureRecognizerResult,
                  unused_output_image: mp.Image, timestamp_ms: int):
    global FPS, COUNTER, START_TIME

    if COUNTER % fps_avg_frame_count == 0:
      FPS = fps_avg_frame_count / (time.time() - START_TIME)
      START_TIME = time.time()

    recognition_result_list.append(result)
    COUNTER += 1

  base_options = python.BaseOptions(model_asset_path=model)
  options = vision.GestureRecognizerOptions(base_options=base_options,
                                            running_mode=vision.RunningMode.LIVE_STREAM,
                                            num_hands=num_hands,
                                            min_hand_detection_confidence=min_hand_detection_confidence,
                                            min_hand_presence_confidence=min_hand_presence_confidence,
                                            min_tracking_confidence=min_tracking_confidence,
                                            result_callback=save_result)
  recognizer = vision.GestureRecognizer.create_from_options(options)

  flag = False
  start_time = 0
  count_time = 0
  detected = False
  flag1 = False
  flag2 = False
  flag3 = False

  while cap.isOpened():
    success, image = cap.read()
    if not success:
      sys.exit(
          'ERROR: Unable to read from webcam. Please verify your webcam settings.'
      )

    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

    recognizer.recognize_async(mp_image, time.time_ns() // 1_000_000)

    current_frame = image

    if recognition_result_list:
      for hand_landmarks in recognition_result_list[0].hand_landmarks:
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y,
                                                z=landmark.z) for landmark in
            hand_landmarks
        ])
        current_frame = cv2.copyMakeBorder(current_frame, 0, label_padding_width,
                                           0, 0,
                                           cv2.BORDER_CONSTANT, None,
                                           label_background_color)

        if recognition_result_list:
          gestures = recognition_result_list[0].gestures

          if gestures:
            category_name = gestures[0][0].category_name
            score = round(gestures[0][0].score, 2)
            result_text = category_name #+ ' (' + str(score) + ')'
            if (category_name == "Closed_Fist"):
              #cnt += 1
              if (flag == False and detected == False):
                start_time = time.time()
                flag = True

            if (((time.time() - start_time) >= 3) and (flag == True)):
              print("Detected for 3 seconds, count down starts")
              detected = True
              count_time = time.time()
              flag = False

        text_size = \
        cv2.getTextSize(result_text, cv2.FONT_HERSHEY_DUPLEX, label_font_size,
                        label_thickness)[0]
        text_width, text_height = text_size

        legend_x = (current_frame.shape[1] - text_width) // 2
        legend_y = current_frame.shape[0] - (
                    label_padding_width - text_height) // 2

        cv2.putText(current_frame, result_text, (legend_x, legend_y),
                    cv2.FONT_HERSHEY_DUPLEX, label_font_size,
                    label_text_color, label_thickness, cv2.LINE_AA)

      recognition_frame = current_frame
      recognition_result_list.clear()

      if (detected):
        if (((time.time() - count_time) >= 1) and flag1 == False):
          print(3)
          flag1 = True
        if (((time.time() - count_time) >= 2) and flag2 == False):
          print(2)
          flag2 = True
        if (((time.time() - count_time) >= 3) and flag3 == False):
          print(1)
          flag3 = True
        if ((time.time() - count_time) >= 4):
          print("Captured")
          current_time = datetime.datetime.now()
          cv2.imwrite(f"./photo/{current_time}.png", image)
          print(f"Photo path ./photo/{current_time}.png")
          detected = False
          flag = False
          flag1 = False
          flag2 = False
          flag3 = False

    if recognition_frame is not None:
        cv2.imshow('gesture_recognition', recognition_frame)

    if cv2.waitKey(1) == 27:
        break

  recognizer.close()
  cap.release()
  cv2.destroyAllWindows()

def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Name of gesture recognition model.',
      required=False,
      default='../model/gesture_recognizer.task')
  parser.add_argument(
      '--numHands',
      help='Max number of hands that can be detected by the recognizer.',
      required=False,
      default=1)
  parser.add_argument(
      '--minHandDetectionConfidence',
      help='The minimum confidence score for hand detection to be considered '
           'successful.',
      required=False,
      default=0.5)
  parser.add_argument(
      '--minHandPresenceConfidence',
      help='The minimum confidence score of hand presence score in the hand '
           'landmark detection.',
      required=False,
      default=0.5)
  parser.add_argument(
      '--minTrackingConfidence',
      help='The minimum confidence score for the hand tracking to be '
           'considered successful.',
      required=False,
      default=0.5)
  parser.add_argument(
      '--cameraId', help='Id of camera.', required=False, default=0)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      default=640)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      default=480)
  args = parser.parse_args()

  run(args.model, int(args.numHands), args.minHandDetectionConfidence,
      args.minHandPresenceConfidence, args.minTrackingConfidence,
      int(args.cameraId), args.frameWidth, args.frameHeight)


if __name__ == '__main__':
  main()

