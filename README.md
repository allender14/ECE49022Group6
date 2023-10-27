# ECE 49022 - Group 6 Smart Tripod

This repository was derived from Tensor Flow Lite's Raspberry Pi sample code found at 
[Tensor Flow Pi example](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi).
This repository uses [TensorFlow Lite](https://tensorflow.org/lite) with Python on
a Raspberry Pi to perform real-time object detection using images streamed from
a USB webcam. It draws a bounding box around one person detected in the camera at a time.

Once a person is detected within the camera frame, instructions our output to center the person 
within the frame. These instructions are computed by taking the difference between the position of
the box and the center of the camera frame. Once centered, a second detection model will take over 
utilizing [MediaPipe Gesture Recognition](https://github.com/googlesamples/mediapipe/tree/main.) 
that will look for a person's closed fist. Once this gesture is detected, it will 
start a countdown timer that will then take a photo of the user. If a photo is taken, or if the 
gesture detection model times out, it will switch back to the object detection model to continue 
detecting a person within the frame.

## Setting up the Hardware

Before you begin, you must
[set up your Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up)
with Raspberry Pi OS (preferably updated to Buster).
For our implementation, we utilized a Raspberry Pi v4 B - 8gb. 

If using the a Pi Camera, you may also need to
[connect and configure the Pi Camera](https://www.raspberrypi.org/documentation/configuration/camera.md).
This code is currently configured to work with a USB camera connected directly to the
Raspberry Pi.

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

Initially we ran into this error after running the setup script:
'ImportError: /lib/arm-linux-gnueabihf/libstdc++.so.6: version `GLIBCXX_3.4.29' not found '.
We found that newer versions of the tflite-support library don't have the required file necessary 
to run the code. To resolve this you can refer to this 
[tflite-support](https://forums.raspberrypi.com/viewtopic.php?t=353534) thread or follow the steps below.
To fix this issue we had to downgrade the version to 0.4.3 in order to get the 
object detection model to work. You can do this by running:

```
python -m pip install --upgrade tflite-support==0.4.3
```

In this project, all you need from the TensorFlow Lite API is the `Interpreter`
class. So instead of installing the large `tensorflow` package, we're using the
much smaller `tflite_runtime` package. The setup scripts automatically install
the TensorFlow Lite runtime.

After that, you need to install `mediapipe`

```
pip install mediapipe
```
However, this will install `opencv-contrib-python`. So, you need to uninstall 

```
pip uninstall opencv-contrib-python opencv-python
```
and reinstall `opencv-contrib-python`

```
pip install opencv-contrib-python
```

## Run the example

```
python3 detect.py \
  --model efficientdet_lite0.tflite
```
