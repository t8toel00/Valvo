#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# TO DO: Make this into a class object with class methods.
# TO DO: Remove logfile from here and switch it into main.py
class mqtt_conn():


    #def __init__(self):

    def connectMqtt(self, addr, port):
        # Open a new sensor "log file" every time we open this program.
        # If the logs directory doesn't exist in the run directory, create one.
        self.client = mqtt.Client()
        self.client.connect(addr,port,60)

    def publishToMqtt(self, topic, msg):
        
        #while msg != "exit":
            #msg=input("Insert a message to send to the topic '" + topic + "': " + chr(10))
        self.client.publish(topic, msg)

    # Close the log file and disconnect from the broker:
    def closeMqtt():
        self.client.disconnect();