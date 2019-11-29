#!/usr/bin/env python3

# Main script for Valvo

import os
import serial
import time
import datetime
from mqtt_publisher import *
from detect_faces import *
import bluetooth
from testBT import *
import select
import queue
import sys
import pysftp        

def handle_read(conn):
    print("Received data:", str(btdata))

def on_connect(client, userdata, flags, rc):
    print("Connected mqtt with result code " + str(rc))

def on_message(client, userdata, msg):
    print("Received message from mqtt: ", msg.payload)
    detectAndSend()

def sendToServer(camData):
    # Print the number of faces and date:
    print(camData[1], " Found ", len(facedata[0]), " persons.")
    print("Time between trigger and finish: " + str(endTime-startTime))
    
    #Publish the data to server and print locally for debug:
    try:
        mqtt_c1.publishToMqtt(topic="raspberry/camera", msg="Tunnistus," + str(facedata[1]) + "," + str(len(facedata[0])))
    except:
        print("Error publishing to mqtt.")
        pass
    
    print("Tunnistus," + str(facedata[1]) + "," + str(len(facedata[0])))
    try:
        #Push snapshot to server:
        sftp.put("snapshots/lastshot.jpg", "/home/ubuntu/www/CodeIgniter/images/" + str(camera1.filename))
    except:
        print("Error pushing file over sftp.")
        pass

def detectAndSend():

    facedata = camera1.snapAndDetect()
    endTime = time.time()
    # Print the number of faces and date:
    print(facedata[1], " Found ", len(facedata[0]), " faces.")
    print("Time between trigger and finish: " + str(endTime-startTime))
    
    #Publish the data to server and print locally for debug:
    try:
        mqtt_c1.publishToMqtt(topic="raspberry/camera", msg="Tunnistus," + str(facedata[1]) + "," + str(len(facedata[0])) + "0")
    except:
        print("Error publishing to mqtt.")
        pass
    
    print("Tunnistus," + str(facedata[1]) + "," + str(len(facedata[0])) + "0")
    try:
        #Push snapshot to server:
        sftp.put("snapshots/lastshot.jpg", "/home/ubuntu/www/CodeIgniter/images/" + str(camera1.filename))
    except:
        print("Error pushing file over sftp.")
        pass




def createConnection(adr):

    # Create new instance of BTConn() class and search for devices.
    connection = BTConn()
    # Get the MAC address of a found device:
    #adr = lookUpNearbyBluetoothDevices()
    7
    logfile.writelines("Connecting to device " + adr)
    print("Connecting to device " + adr)
    # Try to connect and try again if not succesful:
    attempt = 0
    connected = False
    while connected == False:
        
        while connection.connect(address = adr) == False and attempt < 5:
            print("Failed to connect. Retrying...")
            attempt = attempt + 1
            time.sleep(.500)

        if attempt < 5:
            logfile.writelines("Connection successful to device " + adr)
            print("Connection successful to device " + adr)
            connected == True
            return connection
        else:
            #print("Unable to connect to '" + adr + "'. Please choose one manually.")
            #print("Now scanning for nearby devices...")
            #adr = lookUpNearbyBluetoothDevices()
            attempt = 0

def parseData(data):
    # Here we will parse the sensor data we get from arduino:

    return data

# Commonly used flag sets for poll()
READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT
TIMEOUT = 60

mqttPort = 1883
mqttAddress = "172.20.240.54"

sshUsername = "ubuntu"
sshPassword = "beijing12"
sshAddress = "172.20.240.54"

# Declare the queue, which is a list of tuples containing
#   a date and the sensor data and the photo:
sensorQueue = []

if not os.path.exists('logs'):
    os.mkdir('logs')

dt = datetime.datetime.now()
filename = "valvo-log-" + dt.strftime('%Y-%m-%d-%H%M%S')
logfile= open("logs/" + filename, "w")
logfile.writelines(datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S') + "Valvo log started." + chr(10))

# Create new instance of mqtt_conn class and connect to broker
logfile.writelines("Connecting to mqtt broker at address '" + mqttAddress + "' port " + str(mqttPort))
print("Connecting to mqtt broker at address '" + mqttAddress + "' port " + str(mqttPort))
mqtt_c1 = mqtt_conn()
mqtt_c1.client.on_connect = on_connect
mqtt_c1.client.on_message = on_message

# Finally connect to mqtt broker and subscribe to a topic:
mqtt_c1.connectMqtt(addr=mqttAddress,port=mqttPort,topic="server/takephoto")

# Create an sftp connection to the server:
print("Connecting to sftp: " + sshUsername + "@" + sshAddress)
logfile.writelines("Connecting to sftp: " + sshUsername + "@" + sshAddress)
sftp = pysftp.Connection(sshAddress, username = sshUsername, password = sshPassword)


# Then establish bluetooth connections:
arduinoA = createConnection("98:D3:31:B2:B8:D4") #kim-jong-il
#arduinoB = createConnection("98:D3:31:20:40:BB") #kim-jong-un
arduinoB = createConnection("98:D3:31:B2:B9:4C") #kim-jong-ung

arduinoA.handle_read = handle_read

# Set up polling for bluetooth:
poller = select.poll()
poller.register(arduinoA.sock, READ_WRITE)
poller.register(arduinoB.sock, READ_WRITE)

# Map file descriptors to socket objects
fd_to_socket = { arduinoA.sock.fileno(): arduinoA.sock, arduinoB.sock.fileno(): arduinoB.sock,
               }

# Setup camera:
camera1 = cvCam()

# Now we can enter the main loop:
while True:
    # Wait for at least one of the sockets to be ready for processing
    #print >>sys.stderr, '\nwaiting for the next event'
    try:
        arduinoA.sock.getpeername()
    except bluetooth.btcommon.BluetoothError as err:
        logfile.writelines(err)
        print(err)
        arduinoA = createConnection("98:D3:31:B2:B8:D4")
    
    try:
        arduinoB.sock.getpeername()
    except bluetooth.btcommon.BluetoothError as err:
        logfile.writelines(err)
        print(err)
        arduinoB = createConnection("98:D3:31:20:40:BB")
        pass

    events = poller.poll(TIMEOUT)

    # Grab frame but don't save it (to keep buffer running):
    camera1.cam.grab()

    for fd, flag in events:
        # Retrieve the actual socket from its file descriptor
        s = fd_to_socket[fd]

        if flag & (select.POLLIN | select.POLLPRI):
            data = s.recv(1024)

            if data:
                # A readable client socket has data
                startTime = time.time()
                logfile.writelines("Received the following from '" + str(s.getpeername()) + "'.")
                logfile.writelines(str(data))
                print("Received the following from '" + str(s.getpeername()) + "'.")
                print(data)

                # Parse data from received message:
                procData = parseData(data)

                # Take a picture for later detection:
                imageData = camera1.Snap()
                
                image = imageData(2) # Image is the second element of the tuple.
                dt = imageData(3) # Date is the third element of the tuple.

                #Append the sensor data and the photo to the queue for detecting:
                sensorQueue.append((dt, procData, image))

                detectAndSend()



            if len(sensorQueue) > 0:
                #If we have data in queue, process it:


            #else:
                #Refresh the camera so we won't get old images from buffer when trying to actually read:
                
                # Interpret empty result as closed connection
                # print >>sys.stderr, 'closing', client_address, 'after reading no data'
                # Stop listening for input on the connection
                #poller.unregister(s)
                #s.close()
                
                # Remove message queue
                #del message_queues[s]
    
    #time.sleep(0.100)


arduinoA.close()
arduinoB.close()

mqtt_c1.closeMqtt()

# Close the logfile:
logfile.close