#!/usr/bin/env python3

# This script will stay running and snap a picture when needed.
import cv2 
from cv2 import *
import os
import datetime

cam = VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


if not os.path.exists('snapshots'):
    os.mkdir('snapshots')

cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

def snapAndDetect():
    # Snaps a picture when called and tries to detect faces.
    # Returns the amount of faces and possibly the coordinates.
    s, img = cam.read()
    dt = datetime.datetime.now()
    filename = "snapshot-" + dt.strftime('%Y-%m-%d-%H%M%S')
    if s:
        imwrite("snapshots/filename.jpg",img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            #flags = cv2.CV_HAAR_SCALE_IMAGE
            )
        
        print("Found {0} faces!".format(len(faces)))
        for (x, y, w, h) in faces:
           cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        imwrite("snapshots/" + filename + "-detected.jpg",img)
        
        return faces