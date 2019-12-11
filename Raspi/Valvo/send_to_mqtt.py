#!/usr/bin/env python3

# Test script to send mqtt messages.

from mqtt_publisher import *
mqtt_c1 = mqtt_conn()


def on_connect():
    print("connected")

def on_message(client, userdata, msg):
    print("Received message from mqtt: ", msg.payload)



mqtt_c1.client.on_connect = on_connect
mqtt_c1.client.on_message = on_message

top = input("Insert topic you want to send messages to:")
message = ""
mqtt_c1.connectMqtt("172.20.240.55",1883, topic=top)
while message != "exit":
    message=input("Insert a message to send to the topic '" + top + "': " + chr(10))
    mqtt_c1.publishToMqtt(topic=top, msg=message)


mqtt_c1.closeMqtt()
