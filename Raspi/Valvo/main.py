#!/usr/bin/env python3

# Main script for Valvo

import os
import datetime
from mqtt_publisher import *
from detect_faces import snapAndDetect
import bluetooth
from testBT import *
        
        
if not os.path.exists('logs'):
    os.mkdir('logs')

dt = datetime.datetime.now()
filename = "valvo-log-" + dt.strftime('%Y-%m-%d-%H%M%S')
logfile= open("logs/" + filename, "w")
logfile.writelines("Valvo log started.")



if input("Take picture (y/n)?") == "y":
    
    # Snap picture
    facedata = snapAndDetect()

    # Print the number of faces and date:
    print(len(facedata[0]), facedata[1])

if input("Send face data to mqtt?") == "y":
    # Create new instance of mqtt_conn class and connect to broker
    mqtt_c1 = mqtt_conn()
    mqtt_c1.connectMqtt(addr="172.20.240.54",port=1883)
    
    #Publish the data to server and print locally for debug:
    mqtt_c1.publishToMqtt(topic="raspberry/camera", msg="Tunnistus," + str(facedata[1]) + "," + str(len(facedata[0])))
    print("Tunnistus," + str(len(facedata[0])) + "," + str(facedata[1]))
    
    #FORMAT: "table,xxx,xxx,xxx,xxx"
    #Format for camera data: "'Tunnistus',n,yyyy-mm-dd hh:mm:ss.ms,sensor"
    #   ^where n = number of faces, sensor = '0'
    #dateformat: yyyy-mm-dd hh:mm:ss.ms

#sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
if input("Send to BT?") == "y":
    # Create new instance of BTConn() class and search for devices.
    connection = BTConn()
    #BTConn().connect(address=lookUpNearbyBluetoothDevices())
    
    # Get the MAC address of a found device:
    adr = lookUpNearbyBluetoothDevices()

    # Try to connect and try again if not succesful:
    while connection.connect(address = adr) == False:
        print("Failed to connect.")
        #print(connection.connect(address=lookUpNearbyBluetoothDevices()))
    print("Connection successful.")

    # Send Handshake:
    connection.sendMessageTo(targetAddress=adr, mesg="Hello!")
    
    recStr = ""

    # Receive data as long as we don't reveice "Exit" //DOESNT WORK ATM
    #while recStr != "exit":
    #    recBuffer = connection.listenToBT()
    #    recStr = str(recBuffer)
    #    print(recStr)


    connection.close()


# Close the logfile:
logfile.close