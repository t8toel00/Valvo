#!/usr/bin/env python3

# Main script for Valvo

max_ = max
import os
import serial
import time
import datetime
from mqtt_publisher import *
from detect_faces import *
import bluetooth
from BTAsync import *
# import select
import queue
import sys
import pysftp
import threading
from threading import *
import queue
from queue import *
import urllib.request # urllib.request.urlopen(http://ssss.com/?testi=lol)
import operator

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

    if endFlag == True and startFlag == True:
        # Grab frame but don't save it (to keep buffer running):
        camera1.cam.grab()
        imageData = camera1.SnapThree() #snap three images
        #image = imageData[1] # Image is the second element of the tuple.
        images = imageData[1] # Image list is the second element of the tuple.
        dt = imageData[2] # Date is the third element of the tuple.

        # Convert received width to int:
        finalWidth = int(finalStr)

        # Append to queue:
        sensorQueue.put((dt, finalWidth, images))

        btStr = ""
        finalStr = ""
        # Reset the flags:
        startFlag = False
        endFlag = False
    else: 
        print("no endflag")

# def on_BT_read_B(param1,param2):
#     print("Received message from B: ")
#     print("{}{}".format(param1,param2))



#MQTT callback when a connection was established:
def on_connect(client, userdata, flags, rc):
    print("Connected mqtt with result code " + str(rc))

#MQTT callback when a message is received:
def on_message(client, userdata, msg):
    # Grab frame but don't save it (to keep buffer running):
    camera1.cam.grab()
    imageData = camera1.SnapThree() #snap three images
    #image = imageData[1] # Image is the second element of the tuple.
    images = imageData[1] # Image list is the second element of the tuple.
    dt = imageData[2] # Date is the third element of the tuple.

    # Convert received width to int:
    finalWidth = "manual"

    # Append to queue:
    sensorQueue.put((dt, finalWidth, images))
    print("Received message from mqtt: ", msg.payload)
    


def sendToServer(peopleData):
    # peopleData = (date, img, camPeople, senPeople, inPeople, outPeople, width)

    try:
        #Push snapshot to server:
        filename = "snapshot-" + peopleData[0].strftime('%Y-%m-%d-%H%M%S') + "-detected.jpg"
        sftp.put("snapshots/" + filename, "/home/ubuntu/www/CodeIgniter/images/" + filename)
    except:
        print("Error pushing file over sftp.")
        pass

    #Publish the data to server and print locally for debug:
    # Include time, senPeople, inPeople, outPeople, width
    try:
        mqtt_c1.publishToMqtt(topic="raspberry/camera", msg="Tunnistus," + str(peopleData[0]) + "," + str(peopleData[2]) + "," + str(peopleData[3])+ "," + str(peopleData[4]) + "," + str(peopleData[5]) + "," + str(peopleData[6]))
    except:
        print("Error publishing to mqtt.")
        pass



def detectAndSend(data):
    # data is a tuple containing: (date, width, imageList)
    # imageList is a list of images taken sequentially, each item in form: (status, image).
    # so:

    # data
    # --date [0]
    # --width [1]
    # --imageList [2]
    # ----(status0, image0) [0]
    # ----(status1, image1) [1]

    imageLs = data[2]

    # Detect people from image using CV2:
    # Returns a tuple: (faces, bodies)
    # Those include a list of tuples with coordinates:
    # ((xxx, yyy, zzz),(xxx, yyy, zzz))

    # First use the first image...
    camData = camera1.Detect(date = data[0], photo = imageLs[0][1])
    #print(camData)
    #print("faces: ", camData[0])
    #print("bodies: ", camData[1])
    #camFaces = len(camData[0])
    #camBodies = len(camData[1])

    # print("Found", camFaces, " faces.")
    # print("Found", camBodies, " bodies.")

    
    # Determine how many people there are according to ultrasound:
    # Average person width: 40-60 cm
    senWidth = data[1]
    
    if senWidth == "manual":
        senPeople = 0
    else:
        if 75 > senWidth > 15:
            senPeople = 1
        elif 160 > senWidth > 80:
            senPeople = 2
        else:
            senPeople = 0


    camsPeople = []

    # Loop all images and store the amount of people detected in a list:
    for i in range(len(imageLs)):
        camData = camera1.Detect(date = data[0], photo = imageLs[i][1])
        inPeople = 0 
        outPeople = 0
        camFaces = len(camData[0])
        camBodies = len(camData[1])

        print("Found", camFaces, " faces.")
        #print(camData[0])
        print("Found", camBodies, " bodies.")
        #print(camData[1])

        # Loop all bodies:
        for (leftBody, topBody, widthBody, heightBody) in camData[1]:
            bodyFlag = False
            faceFlag = False

            # Loop all faces:
            for (left,top,width,height) in camData[0]:
                # print(left, leftBody, top, topBody, (left+width), (leftBody + widthBody), (top + height), (topBody + heightBody))
                # print((left >= leftBody), (top >= topBody), ((left + width) <= (leftBody + widthBody)), ((top + height) <= (topBody + heightBody)))
                # If the body has a face in it:
                if left >= leftBody and top >= topBody and (left + width) <= (leftBody + widthBody) and (top + height) <= (topBody + heightBody):
                    print("face found inside body")
                    # If a face was not in this body yet:
                    if faceFlag == False:
                        # If the body was detected as outgoing before:
                        if bodyFlag == True:
                            outPeople = outPeople - 1
                            inPeople = inPeople + 1
                            bodyFlag = True
                            faceFlag = True
                        else:
                            inPeople = inPeople + 1
                            bodyFlag = True
                            faceFlag = True
                            camera1.drawBox(camData[2], leftBody, topBody, widthBody, heightBody)

                # If the body doesn't have a face in it this loop:
                else:
                    if bodyFlag == False and faceFlag == False:
                        outPeople = outPeople + 1
                        bodyFlag = True
                        camera1.drawBox(camData[2], leftBody, topBody, widthBody, heightBody)
            # If there were no faces, just add the person as an outgoer:
            if len(camData[0]) == 0:
                outPeople = outPeople + 1

        # Finally append the data for this image and the image as the last item:
        camsPeople.append((inPeople, outPeople, camData[2]))
        print("In ppl: ", inPeople, ". Out ppl: ", outPeople)


    # Combine in and outgoing people for now:
    camPeople = camsPeople[0][0] + camsPeople[0][1]

    # if camPeople == senPeople:
    #     people = camPeople
    #     rImage = imageLs[0][1]
# else:
    print("Camera detected different amount of people!")

    # Choose the most likely correct result from all images:
    dPeople = {}

    # Cycle through all the image data,
    #   and count how many same items there are...
    for inP, outP, img in camsPeople:

        if str(inP) + "," + str(outP) in dPeople:
            dPeople[str(inP) + "," + str(outP)] = dPeople[str(inP) + "," + str(outP)] + 1
        else:
            dPeople[str(inP) + "," + str(outP)] = 1

    # Now check which item of dPeople has the largest value:
    #k = max(dPeople, key=lambda key: dPeople[key])
    print("dPeople: ",dPeople)
    k = max_(dPeople, key=dPeople.get)
    #k = max(dPeople.items(), key=operator.itemgetter(1))[0]
    klist = k.split(',')
    inPeople = int(klist[0])
    outPeople = int(klist[1])
    
    print("most popular pair (i/o): ", k)
    print("in ppl.: ", inPeople)
    print("out ppl.: ", outPeople)
    people = inPeople + outPeople
    
    # Determine the photo we will return:
    for x in range(len(camsPeople)):
        if camsPeople[x][0] == inPeople and camsPeople[x][1] == outPeople:
            rImage = camsPeople[x][2]
    # rImage = 
    # people = 0
    #print("Camera people: ", camPeople, ". Sensor people: ", senPeople)
        

    # Return amount of people detected by sensor, by camera,
    #   the assumed direction (and number to each direction???) and date and image:
    # (date, img, camPeople, senPeople, inPeople, outPeople)
    returnData = tuple((data[0], rImage, camPeople, senPeople, inPeople, outPeople, senWidth))

    # Save the image we used for detection (or any...)
    filename = "snapshot-" + data[0].strftime('%Y-%m-%d-%H%M%S') + "-detected.jpg"
    imwrite("snapshots/" + filename, rImage)

    sendToServer(returnData)


    # # HTTP DEMO:
    # payload = "'people':5"
    # payload = payload.encode('utf-8')
    # # Push the data to HTTP GET
    # urllib.request.urlopen("http://172.20.240.54/testi/dbInsert.php?people=" + str(people))
    # #r = urllib.request.urlopen("http://172.20.240.54/testi/dbInsert.php", data=payload)
    # #print(r)

    return returnData


def handle_detect(x, y, z, a, b, c, d):
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
#arduinoA = createConnection("98:D3:31:20:40:BB") #kim-jong-un
#arduinoB = createConnection("98:D3:31:B2:B9:4C") #kim-jong-ung

btThreadA = BaseThread(
    name='btA',
    target=arduinoA.read_from_bluetooth,
    #loop=True,
    callback=on_BT_read_A
)

btThreadA.loop = True

# btThreadB = BaseThread(
#     name='btB',
#     target=arduinoB.read_from_bluetooth,
#     #loop=True,
#     callback=on_BT_read_B
# )
# btThreadB.loop = True



#Start bluetooth threads:
btThreadA.start()
# btThreadB.start()


thrIndex = 0

print("Entering main loop")

# Now we can enter the main loop:
while True:

    try:
        arduinoA.sock.getpeername()
    except bluetooth.btcommon.BluetoothError as err:
        #logfile.writelines(err)
        print("Connectiong lost:")
        print(err)
        arduinoA = createConnection("98:D3:31:B2:B8:D4")
    
    # try:
    #     arduinoB.sock.getpeername()
    # except bluetooth.btcommon.BluetoothError as err:
    #     logfile.writelines(err)
    #     print("Connection lost:")
    #     print(err)
    #     arduinoB = createConnection("98:D3:31:20:40:BB")
    #     pass

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
# arduinoB.close()

mqtt_c1.closeMqtt()

# Close the logfile:
logfile.close