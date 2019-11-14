#!/usr/bin/env python3

# Test script to send mqtt messages.

from mqtt_publisher import publishToMqtt
connectMqtt("172.20.240.54",1883)

top = input("Insert topic you want to send messages to:")

publishToMqtt(top)

closeMqtt()
