# Bioloid-Dynamixel-AX12A

## Requirements:

**Software:**
```bash
Python 
```

**Import Libraries:**
```bash
Matplotlib, PyLab, Threading, Serial, NumPy, OpenCV, Tkinter 
```
# OpenCV Test (Logitech Webcam C930e) 

```bash
[ check_fps.py        ] Find frames per second (fps) in OpenCV.
[ object_detection.py ] Find the HSV parameters for the color of each object.
[ check_result.py     ] Check the previously detected HSV parameters.
```

Directory:
[Camera Test](https://github.com/rparak/Bioloid-Dynamixel-AX12A/tree/master/Camera_test)

# Simple testing - control of Dynamixel AX-12A servo motors using Python's own library

The project demonstrates the control of AX-12A servomotors on several examples. Dynamixel doesn’t respond to PWM signals, but a slightly more complicated protocol of instructions for reading and writing onto its memory. This communication happens over a half-duplex UART 
port, using only one wire for both sending and receiving. Control of Dynamixel AX-12A servo 
motors using Python's own library. Communication with the control system is via USB.

<p align="center">
<img src="https://github.com/rparak/Bioloid-Dynamixel-AX12A/blob/master/images/bioloid_all_1_fig.PNG" width="700" height="500">
</p>

## Connection:

<p align="center">
<img src="https://github.com/rparak/Bioloid-Dynamixel-AX12A/blob/master/images/connection_fig.png" width="700" height="350">
</p>

## Step no. 1: Control one servo motor
* TKinter, python animation
* OpenCV (multiple object tracking), matplotlib

<p align="center">
<img src="https://github.com/rparak/Bioloid-Dynamixel-AX12A/blob/master/images/step_11_fig.png" width="700" height="350">
</p>

<p align="center">
<img src="https://github.com/rparak/Bioloid-Dynamixel-AX12A/blob/master/images/step_12_fig.png" width="700" height="300">
</p>

## Step no. 2: Control Bioloid Humanoid
* OpenCV (multiple object tracking), matplotlib

<p align="center">
<img src="https://github.com/rparak/Bioloid-Dynamixel-AX12A/blob/master/images/step_2_fig.png" width="700" height="350">
</p>

## Step no. 3: Control King-Spider
* OpenCV (object tracking), matplotlib

<p align="right">
<img src="https://github.com/rparak/Bioloid-Dynamixel-AX12A/blob/master/images/step_3_fig.png" width="700" height="350">
</p>

## Result:

Youtube: https://www.youtube.com/watch?v=c92E_YC9uZQ

## Contact Info:
Roman.Parak@outlook.com

## Citation (BibTex)

```bash
@misc{RomanParak_AX12A,
  author = {Roman Parak},
  title = {An open-source library to control the ax-12a servomotor},
  year = {2019-2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/rparak/Bioloid-Dynamixel-AX12A}}
}
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
