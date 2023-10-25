# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utility functions to display the pose detection results."""

import cv2
import numpy as np
from tflite_support.task import processor

_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (0, 0, 255)  # red


def visualize(
    image: np.ndarray,
    detection_result: processor.DetectionResult,
) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.

  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.

  Returns:
    Image with bounding boxes.
  """
  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 3)

    # Draw label and score
    category = detection.categories[0]
    category_name = category.category_name
    probability = round(category.score, 2)
    result_text = category_name + ' (' + str(probability) + ')'
    text_location = (_MARGIN + bbox.origin_x,
                     _MARGIN + _ROW_SIZE + bbox.origin_y)
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)

  return image

def adjust_camera_position(detection_result: processor.DetectionResult, width, height):
     # Intializie servo control commands
    horizontal_command = 0
    vertical_command = 0
        
    for detection in detection_result.detections:
        # Draw bounding_box
        bbox = detection.bounding_box
        
        # Get first bounding box from the detection list and extract the x and y coordinates
        bbox_x_center = bbox.width / 2 + bbox.origin_x
        bbox_y_center = bbox.height / 2 + bbox.origin_y
        
        # Get the center of the camera frame
        frame_center_x = width / 2
        frame_center_y = 2 * height / 3
        
        # Calculate the difference between teh center of the bounding box and the frame center
        delta_x = bbox_x_center - frame_center_x
        delta_y = bbox_y_center - frame_center_y
        
        # Definte movement threshold for how centered object should be
        x_threshold = 50
        y_threshold = 20
        
        # Determine the x and y camera movements
        if abs(delta_x) > x_threshold:
            # Move the camera horizontally to center the object
            horizontal_command = delta_x / width
            #if(horizontal_command > 0):
                #print('Move camera left')
            #else:
                #print('Move camera right')
        #else:
            #print('Object horizontally centered')
        
        if abs(delta_y) > y_threshold:
            # Move the camera vertically to center the object
            vertical_command = delta_y / height
            #if(vertical_command > 0):
                #print('Move camera down')
            #else:
                #print('Move camera up')
        #else:
            #print('Object vertically centered')        
        
        
    return horizontal_command, vertical_command
    
    
    
    
    
