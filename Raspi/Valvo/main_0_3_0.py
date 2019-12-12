#!/usr/bin/env python3

# Main script for Valvo

import os
import serial
import time
import datetime
from mqtt_publisher import *
from detect_faces import *
import bluetooth
# from testBT import *
from BTAsync import *
# import select
import queue
import sys
import pysftp
import threading
from threading import *
import queue
from queue import *

# Thread class with callback:
class BaseThread(threading.Thread):

    def __init__(self, callback=None, callback_args=None, *args, **kwargs):
        target = kwargs.pop('target')
        cls = self.__class__
        #self.__class__.stop_event.clear()
        super(BaseThread, self).__init__(target=self.target_with_callback, *args, **kwargs)
        self.callback = callback
        self.method = target
        self.loop = False
        self.stop_event = threading.Event()
        self.stop_event.clear()
        #self.callback_args = callback_args
    
    #@classmethod
    def stop_thread(self):
        #cls.stop_event.set()
        self.stop_event.set()
    
    def target_with_callback(self, arg = None):
        cls = self.__class__
        while not self.stop_event.is_set():
            if arg == None:
                self.callback_args = self.method()
            if arg != None:
                self.callback_args = self.method(arg)
            if self.callback is not None:
                self.callback(*self.callback_args)
            if self.loop == False:
                self.stop_thread()


startFlag = False
endFlag = False
finalStr = ""

#Bluetooth callbacks:
#MAKE THIS A THREAD INSTEAD??
def on_BT_read_A(param1, param2):
    print("Received message from A: ")
    print(param2)
    print("{} {}".format(param1, param2))

    global startFlag
    global endFlag
    global finalStr

    formStr = format(param2)

    try: finalStr
    except:
        finalStr = ""

    try: btStr
    except:
        btStr = ""
    
    # Delete the identifying characters (b'[xxx]'=>[xxx])
    for c in range(2, len(formStr)-1):
        btStr = btStr + formStr[c]

    # Append data as long as we receive end flag "]"
    # TODO: ...and start new string if we receive "["
    if endFlag == False:
        for c in btStr:
            if c == chr(91): # "["
                startFlag = True
            elif c == chr(93):  # "]"
                endFlag = True
                #lsFinal = [finalStr]
            else:
                if startFlag == True:
                    finalStr = finalStr + c
    elif endFlag == False and startFlag == False:
        finalStr = ""
    
    print("paastiin tanne asti")
    print(startFlag)
    print(endFlag)

    if endFlag == True and startFlag == True:
        # Grab frame but don't save it (to keep buffer running):
        camera1.cam.grab()
        imageData = camera1.Snap() 
        image = imageData[1] # Image is the second element of the tuple.
        dt = imageData[2] # Date is the third element of the tuple.

        # Convert received width to int:
        finalWidth = int(finalStr)

        # Append to queue:
        #sensorQueue.append((dt, finalStr, image))
        sensorQueue.put((dt, finalWidth, image))

        btStr = ""
        finalStr = ""
        # Reset the flags:
        startFlag = False
        endFlag = False
    else: 
        print("no endflag")

def on_BT_read_B(param1,param2):
    print("Received message from B: ")
    print("{}{}".format(param1,param2))



#MQTT callbacks:
def on_connect(client, userdata, flags, rc):
    print("Connected mqtt with result code " + str(rc))

#MQTT 
def on_message(client, userdata, msg):
    print("Received message from mqtt: ", msg.payload)
    #detectAndSend()


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



def detectAndSend(data):
    # data is a tuple containing: (date, width, image)
    # Detect people from image using CV2:
    # Returns a tuple: (faces, bodies)
    # Those include a list of tuples with coordinates:
    # ((xxx, yyy, zzz),(xxx, yyy, zzz))

    camData = camera1.Detect(date = data[0], photo = data[2])
    print(camData)
    camFaces = len(camData[0])
    camBodies = len(camData[1])

    print("Found", camFaces, " faces.")
    print("Found", camBodies, " bodies.")

    # Compare people count that the camera found against ultrasound sensors:
    # Average person width: 40-60 cm
    width = data[1]

    if 75 > width > 30:
        senPeople = 1
    elif 150 > width > 80:
        senPeople = 2
    else:
        senPeople = 0


    if camBodies == camFaces:
        camPeople = camBodies
    else:
        camPeople = camBodies


    if camPeople == senPeople:
        people = camBodies
    else:
        people = 0

    # Return amount of people detected by sensor, by camera,
    #   the assumed direction (and number to each direction???) and date and image:
    # (date, img, camPeople, senPeople)
    returnData = tuple((data[0], data[2], camPeople, senPeople, people))

    try:
        #Push snapshot to server:
        filename = "snapshot-" + data[0].strftime('%Y-%m-%d-%H%M%S') + "-detected.jpg"
        sftp.put("snapshots/" + filename, "/home/ubuntu/www/CodeIgniter/images/" + filename)
    except:
        print("Error pushing file over sftp.")
        pass

    #Publish the data to server and print locally for debug:
    try:
        mqtt_c1.publishToMqtt(topic="raspberry/camera", msg="Tunnistus," + str(data[0]) + "," + str(camPeople) + "," + str(senPeople))
    except:
        print("Error publishing to mqtt.")
        pass

    return returnData


def handle_detect(x, y, z, a, b):
    # This callback function is called when detection algorithm has been run.
    # Handle sending data here??
    print("Detect done")



def createConnection(adr):

    # Create new instance of BTConn() class and search for devices.
    connection = BTConn()
    # Get the MAC address of a found device:
    #adr = lookUpNearbyBluetoothDevices()
    
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
# READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
# READ_WRITE = READ_ONLY | select.POLLOUT
# TIMEOUT = 60

# Setup camera:
camera1 = cvCam()

mqttPort = 1883
mqttAddress = "172.20.240.54"

sshUsername = "ubuntu"
sshPassword = "beijing12"
sshAddress = "172.20.240.54"

# Declare the queue, which is a list of tuples containing
#   a date and the sensor data and the photo:
#sensorQueue = []
sensorQueue = queue.Queue()
qIndex = 0

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
arduinoB = createConnection("98:D3:31:20:40:BB") #kim-jong-un
#arduinoB = createConnection("98:D3:31:B2:B9:4C") #kim-jong-ung

btThreadA = BaseThread(
    name='btA',
    target=arduinoA.read_from_bluetooth,
    #loop=True,
    callback=on_BT_read_A
)

btThreadA.loop = True

btThreadB = BaseThread(
    name='btB',
    target=arduinoB.read_from_bluetooth,
    #loop=True,
    callback=on_BT_read_B
)
btThreadB.loop = True



#Start bluetooth threads:
btThreadA.start()
btThreadB.start()

# Map file descriptors to socket objects
fd_to_socket = { arduinoA.sock.fileno(): arduinoA.sock, arduinoB.sock.fileno(): arduinoB.sock,
               }



thrIndex = 0

print("Entering main loop")

# Now we can enter the main loop:
while True:

    try:
        arduinoA.sock.getpeername()
    except bluetooth.btcommon.BluetoothError as err:
        logfile.writelines(err)
        print("Connectiong lost:")
        print(err)
        arduinoA = createConnection("98:D3:31:B2:B8:D4")
    
    try:
        arduinoB.sock.getpeername()
    except bluetooth.btcommon.BluetoothError as err:
        logfile.writelines(err)
        print("Connection lost:")
        print(err)
        arduinoB = createConnection("98:D3:31:20:40:BB")
        pass

    #events = poller.poll(TIMEOUT)

    if sensorQueue.qsize() != 0:
        
        #If we have data in queue, process it:
        print("data in queue:")
        #qIndex = qIndex - 1

        arguments = (sensorQueue.get(),)
        thrIndex = thrIndex + 1
        
        dtThread = BaseThread(
                    name='detectThrd' + str(thrIndex),
                    target=detectAndSend,
                    args=arguments,
                    callback=handle_detect
                    )
        dtThread.start()
        # Wait for the detect thread to complete; we only want one running at a time.
        dtThread.join()

    #time.sleep(0.01)
    #print("looping")


arduinoA.close()
arduinoB.close()

mqtt_c1.closeMqtt()

# Close the logfile:
logfile.close