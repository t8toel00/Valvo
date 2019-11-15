#!/usr/bin/env python3

# Test script to send mqtt messages.

from mqtt_publisher import publishToMqtt

top = input("Insert topic you want to send messages to:")

publishToMqtt(top)