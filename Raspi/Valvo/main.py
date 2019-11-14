#!/usr/bin/env python3

# Main script for Valvo

from mqtt_publisher import publishToMqtt
from detect_faces import snapAndDetect
import bluetooth
from testBT import *



if input("Take picture (y/n)?") == "y":
    
    # Snap picture
    faces = snapAndDetect()

    # Print the number of faces:
    print(len(faces))

if input("Send face data to mqtt?") == "y":
    publishToMqtt("raspberry/camera", faces)

    #FORMAT: "table,xxx,xxx,xxx,xxx"
    #dateformat: yyyy-mm-dd hh:mm:ss.ms
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
if input("Send to BT?") == "y":
    connection = BTConn()
    #BTConn().connect(address=lookUpNearbyBluetoothDevices())
    while BTConn().connect(address=lookUpNearbyBluetoothDevices()) == False:
        print("Failed to connect.")
        #print(connection.connect(address=lookUpNearbyBluetoothDevices()))
    print("Connection successful.")
