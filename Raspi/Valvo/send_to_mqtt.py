#!/usr/bin/env python3

# Test script to send mqtt messages.

from mqtt_publisher import *
mqtt_c1 = mqtt_conn()

mqtt_c1.connectMqtt("172.20.240.54",1883)

top = input("Insert topic you want to send messages to:")
message = ""
while message != "exit":
    message=input("Insert a message to send to the topic '" + top + "': " + chr(10))
    mqtt_c1.publishToMqtt(topic=top, msg=message)


mqtt_c1.closeMqtt()
