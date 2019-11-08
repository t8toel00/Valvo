#!/usr/bin/env python3

# Main script for Valvo

from mqtt_publisher import publishToMqtt
from detect_faces import snapAndDetect

if input("Take picture (y/n)?") == "y":
    snapAndDetect()
    #pygame.image.save(img,"Test.jpg")