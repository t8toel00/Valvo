#!/usr/bin/env python3

import os

import paho.mqtt.client as mqtt
import datetime
# Add reading sensor data directly from arduino modules, then save them to a file AND send them forward!

# Add camera data too.



def publishToMqtt(topic):
    
    # Open a new sensor "log file" every time we open this program.
    # If the logs directory doesn't exist in the run directory, create one.
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    dt = datetime.datetime.now()
    filename = "valvo-log-" + dt.strftime('%Y-%m-%d-%H:%M:%S')
    logfile= open("logs/" + filename, "w")
    logfile.writelines("Valvo mqtt publisher log started.")

    client = mqtt.Client()
    client.connect("172.20.240.54",1883,60)
    msg = ""
    while msg != "exit":
        msg=input("Insert message you want to send to topic (write exit to exit) '" + topic + "': " + chr(10))
        logfile.writelines(msg + "\n")
        client.publish(topic, msg)

# Close the log file and disconnect from the broker:
def closeMqtt():
    logfile.close
    client.disconnect();