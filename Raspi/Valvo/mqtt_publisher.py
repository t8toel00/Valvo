#!/usr/bin/env python3

import os
import paho.mqtt.client as mqtt
import datetime
dt = datetime.datetime.now()
# Add reading sensor data directly from arduino modules, then save them to a file AND send them forward!

# Open a new sensor "log file" every time we open this program.
# If the logs directory doesn't exist in the run directory, create one.
if not os.path.exists('logs'):
    os.mkdir('logs')

filename = "valvo-log-" + dt.strftime('%Y-%m-%d-%H:%M:%S')
logfile= open("logs/" + filename, "w")
logfile.writelines("Valvo mqtt publisher log started.")
msg="PLACEHOLDER"
topic = "raspberry/sensor"

client = mqtt.Client()
client.connect("172.20.240.54",1883,60)

while msg != "exit":
    msg=input("Insert message you want to send to topic '" + topic + "': " + chr(10))
    logfile.writelines(msg + "\n")
    client.publish(topic, msg)

# Close the log file and disconnect from the broker:
logfile.close
client.disconnect();