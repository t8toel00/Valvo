#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# TO DO: Make this into a class object with class methods.
# TO DO: Remove logfile from here and switch it into main.py
class mqtt_conn():


    def __init__(self):
        self.client = mqtt.Client()

    def connectMqtt(self, addr, port, topic, qos=0):
        self.client.connect(addr,port,60)
        self.client.subscribe(topic, qos)
        self.client.loop_start()

    def publishToMqtt(self, topic, msg, qos=0):
        self.client.publish(topic, msg, qos)

    #def subscribeToMqtt(self, topic, qos=0):
    #    try:
    #        self.client.subscribe(topic, qos)

    # Close the log file and disconnect from the broker:
    def closeMqtt():
        self.client.loop_stop()
        self.client.disconnect();
