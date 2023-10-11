# ECE 49022 - Group 6 Smart Tripod

This repository was derived from Tensor Flow Lite's Raspberry Pi sample code found at 
[Tensor Flow Pi example](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi).
This repository uses [TensorFlow Lite](https://tensorflow.org/lite) with Python on
a Raspberry Pi to perform real-time object detection using images streamed from
a USB webcam. It draws a bounding box around one person detected in the camera at a time.

Once a person is detected within the camera frame, instructions our output to center the person 
within the frame. Once centered, a second detections model will take over utilizing () that will 
look for a person's closed fist. Once this gesture is detected, it will start a countdown timer
that will then take a photo of a user. If a photo is taken, or if the gesture detection model 
times out, it will switch back to the object detections model to continue detecting a person 
within the frame.

## Setting up the Hardware

Before you begin, you must
[set up your Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up)
with Raspberry Pi OS (preferably updated to Buster).
For our implementation, we utilized a Raspberry Pi v4 B - 8gb. 

You may also need to
[connect and configure the Pi Camera](https://www.raspberrypi.org/documentation/configuration/camera.md)
if you use the Pi Camera. This code also works with USB camera connect to the
Raspberry Pi.
For our implementation, we just used a USB webcam that was plugged directly into the Pi.

## Running the code

First, clone this Git repo onto your Raspberry Pi.

It is recommended to setup a python virtual environment.
Then use the script to install a couple Python packages, and download the
EfficientDet-Lite model:

```
cd examples/lite/examples/object_detection/raspberry_pi

# The script install the required dependencies and download the TFLite models.
sh setup.sh
```

We initially had issues getting the model running because the neweer versions of 
[]() were no compatible. We had to downgrade the version to __ in order to get the 
object detection model to work. 

In this project, all you need from the TensorFlow Lite API is the `Interpreter`
class. So instead of installing the large `tensorflow` package, we're using the
much smaller `tflite_runtime` package. The setup scripts automatically install
the TensorFlow Lite runtime.

## Run the example

```
python3 detect.py \
  --model efficientdet_lite0.tflite
```
