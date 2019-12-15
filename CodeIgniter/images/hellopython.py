#!/usr/bin/env python3

print("importing client")

import sys
print(sys.path)

import paho.mqtt.client as mqtt

print("Sending request ")
client = mqtt.Client()
client.connect("127.0.0.1",1883,60)
client.publish("server/takephoto", "1")
print("Request sent ")
client.disconnect()