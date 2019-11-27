#!/usr/bin/env python3

# This script will stay running and snap a picture when needed.
import cv2 
from cv2 import *
import os
import datetime




if not os.path.exists('snapshots'):
    os.mkdir('snapshots')

class cvCam():

    def __init__(self):
        # Create the haar cascade
        #self.cascPath = "haarcascade_frontalface_default.xml"
        #self.cascPath = "haarcascade_fullbody.xml"
        self.cascPath = "haarcascade_upperbody.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascPath)
        self.cam = VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cam.grab()

    def snapAndDetect(self):

        # Snaps a picture when called and tries to detect faces.
        # Returns the amount of faces and possibly the coordinates.
        self.s, self.img = self.cam.read()
        self.dt = datetime.datetime.now()
        self.filename = "snapshot-" + self.dt.strftime('%Y-%m-%d-%H%M%S') + "-detected.jpg"
        if self.s:
            #imwrite("snapshots/filename.jpg",img)
            self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.faces = self.faceCascade.detectMultiScale(
                self.gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                #flags = cv2.CV_HAAR_SCALE_IMAGE
                )
            
            #print("Found {0} faces!".format(len(self.faces)))
            for (x, y, w, h) in self.faces:
                cv2.rectangle(self.img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            imwrite("snapshots/" + self.filename,self.img)
            imwrite("snapshots/lastshot.jpg",self.img)
            
            # Release the video stream:
            #cam.release()

            # Finally, return the amount of faces, timestamp and the trigger source:
            return self.faces, self.dt
        