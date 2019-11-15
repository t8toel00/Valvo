#!/usr/bin/env python3

# Main script for Valvo

from mqtt_publisher import *
from detect_faces import snapAndDetect
import bluetooth
from testBT import *



if input("Take picture (y/n)?") == "y":
    
    # Snap picture
    facedata = snapAndDetect()

    # Print the number of faces and date:
    print(len(facedata[0]), facedata[1])

if input("Send face data to mqtt?") == "y":
    mqtt_c1 = mqtt_conn()
    mqtt_c1.connectMqtt(addr="172.20.240.54",port=1883)
    mqtt_c1.publishToMqtt(topic="raspberry/camera", msg="Tunnistus," + str(len(facedata[0])) + "," + str(facedata[1]))
    print("Tunnistus," + str(len(facedata[0])) + "," + str(facedata[1]))
    #FORMAT: "table,xxx,xxx,xxx,xxx"
    #dateformat: yyyy-mm-dd hh:mm:ss.ms

#sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
if input("Send to BT?") == "y":
    connection = BTConn()
    #BTConn().connect(address=lookUpNearbyBluetoothDevices())
    while BTConn().connect(address=lookUpNearbyBluetoothDevices()) == False:
        print("Failed to connect.")
        #print(connection.connect(address=lookUpNearbyBluetoothDevices()))
    print("Connection successful.")
