#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Publisher

client = mqtt.Client()
client.connect("127.0.0.1",1883,60)
client.publish("server/takephoto", "1")
print("Request sent")
client.disconnect()