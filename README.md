# Valvo
OAMK ICT project 2019

This device is for monitoring pedestrian traffic on a hallway. It's capable of recognizing the number of people going through as well as their heading (in/out).



## Setup for Raspberry Pi:
You will need a linux-capable computer to run the monitoring scripts.
You will need a Python3 environment with all the required modules.
You will need a USB Webcam.
You will need to install v4l2 for the camera to work (if your linux distribution doesn't already have it).

Main.py is the main script which will call all the other scripts when necessary.

Python modules needed (+ any that python reports as missing):
`serial mqtt cv2 pysftp pybluez paho-mqtt`

**Installation process:**
1) Install Python3, preferably version 3.7.3.
2) Copy main.py, mqtt_publisher.py, BTAsync.py, detect_faces.py,
haarcascade_frontalface_default.xml and haarcascade_upperbody.xml 
into a folder where you can run python scripts.
3) Run `python3 main.py`


## Setup for Server



## Setup for Arduino
