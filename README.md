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
The project was run by: 

Server -> Ubuntu 18.04.3 LTS

Database -> Mysql 5.7.28

Web page -> CodeIgniter 3.1.5

Others -> Python 3 (3.6.8)  -> pip install paho-mqtt
                            -> pip install mysql-connector 

       -> Jpegoptim

To get a working "Take a photo"-button in the web page, copy paho-mqtt pip-files to:
(or you can try existing files from Github and see if they work)

CodeIgniter/images/paho

CodeIgniter/images/paho_mqtt-1.5.0.egg-info

CodeIgniter/images/paho_mqtt-1.5.0.dist-info

Make sure these files have web-user execute access 775

**Important files on Server:**
/home/ubuntu/mqtt/subscriber10.py -> Listens on detect-messages from Pi's main.py and inserts them to the database, set your DB-login here
(file can be found at Mysql-folder, place it in any directory you like on your server)

/www/CodeIgniter/application/controllers/Valvo.php -> The whole web content in one file, you're welcome ;)

/www/CodeIgniter/images/hellopython.py -> Sends a MQTT message to Pi when "Take a photo" is pressed
/www/CodeIgniter/images/compressJpeg.sh -> A shell command to run Jpegoptim on images-folder (compress to 65-75 Kb) when "Compress images" is pressed
Make sure these files have web-user execute access 775

/www/CodeIgniter/application/application/config/autoload.php
/www/CodeIgniter/application/application/config/config.php -> Set your base URL, you have to Find & Replace "http://172.20.240.54/" to your address in Valvo.php
/www/CodeIgniter/application/application/config/database.php -> Change your user & pw if needed, defaults are localhost, user: admin, pw: beijing12

**Installation:**
1) Install programs listed above
2) Replace important files with downloaded ones
3) Adjust needed settings, remember user privileges
4) Run `python3 subscriber10.py`

## Setup for Arduino
