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
        

# Commonly used flag sets for poll()
READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT
TIMEOUT = 60

mqttPort = 1883
mqttAddress = "172.20.240.54"

if not os.path.exists('logs'):
    os.mkdir('logs')

dt = datetime.datetime.now()
filename = "valvo-log-" + dt.strftime('%Y-%m-%d-%H%M%S')
logfile= open("logs/" + filename, "w")
logfile.writelines("Valvo log started.")

# Create new instance of mqtt_conn class and connect to broker
print("Connecting to mqtt broker at address '" + mqttAddress + "' port " + str(mqttPort))
mqtt_c1 = mqtt_conn()
mqtt_c1.connectMqtt(addr=mqttAddress,port=mqttPort)


def createConnection(adr):

    # Create new instance of BTConn() class and search for devices.
    connection = BTConn()
    # Get the MAC address of a found device:
    #adr = lookUpNearbyBluetoothDevices()

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
            print("Connection successful to device " + adr)
            connected == True
            return connection
        else:
            #print("Unable to connect to '" + adr + "'. Please choose one manually.")
            #print("Now scanning for nearby devices...")
            #adr = lookUpNearbyBluetoothDevices()
            attempt = 0

        
# Then establish bluetooth connections:
arduinoA = createConnection("98:D3:31:B2:B8:D4") #kim-jong-il
arduinoB = createConnection("98:D3:31:20:40:BB") #kim-jong-un
#arduinoB = createConnection("98:D3:31:B2:B9:4C") #HC-06

# Set up polling for bluetooth:
poller = select.poll()
poller.register(arduinoA.sock, READ_WRITE)
poller.register(arduinoB.sock, READ_WRITE)

# Map file descriptors to socket objects
fd_to_socket = { arduinoA.sock.fileno(): arduinoA.sock, arduinoB.sock.fileno(): arduinoB.sock,
               }

# Now we can enter the main loop:

while True:
    # Wait for at least one of the sockets to be ready for processing
    #print >>sys.stderr, '\nwaiting for the next event'
    try:
        arduinoA.sock.getpeername()
    except bluetooth.btcommon.BluetoothError as err:
        print(err)
        arduinoA = createConnection("98:D3:31:B2:B8:D4")
    
    try:
        arduinoB.sock.getpeername()
    except bluetooth.btcommon.BluetoothError as err:
        print(err)
        arduinoB = createConnection("98:D3:31:20:40:BB")
        pass

    events = poller.poll(TIMEOUT)

    for fd, flag in events:
        # Retrieve the actual socket from its file descriptor
        s = fd_to_socket[fd]

        if flag & (select.POLLIN | select.POLLPRI):
            data = s.recv(1024)

            if data:
                # A readable client socket has data
                #message_queues[s].put(data)
                print("Received the following from '" + str(s.getpeername()) + "'.")
                print(data)

                if data:
                    facedata = snapAndDetect()
                    # Print the number of faces and date:
                    print(len(facedata[0]), facedata[1])
                    
                    #Publish the data to server and print locally for debug:
                    mqtt_c1.publishToMqtt(topic="raspberry/camera", msg="Tunnistus," + str(facedata[1]) + "," + str(len(facedata[0])))
                    print("Tunnistus," + str(facedata[1]) + "," + str(len(facedata[0])))

                    #FORMAT: "table,xxx,xxx,xxx,xxx"
                    #Format for camera data: "'Tunnistus',n,yyyy-mm-dd hh:mm:ss.ms,sensor"
                    #   ^where n = number of faces, sensor = '0'
                    #dateformat: yyyy-mm-dd hh:mm:ss.ms

            #else:
                # Interpret empty result as closed connection
                # print >>sys.stderr, 'closing', client_address, 'after reading no data'
                # Stop listening for input on the connection
                #poller.unregister(s)
                #s.close()
                
                # Remove message queue
                #del message_queues[s]
    
    time.sleep(0.500)


arduinoA.close()
arduinoB.close()

# Close the logfile:
logfile.close