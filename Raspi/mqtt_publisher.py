#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Publisher

client = mqtt.Client()
client.connect("172.20.240.54",1883,60)
client.publish("raspberry/kamera", "exit");

client.disconnect();