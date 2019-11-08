#!/usr/bin/env python3
# tee viesteistä loki, muotoile ne SQL-komennoiksi ja lähetä ne tietokantaan

import paho.mqtt.client as mqtt

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("raspberry/+")

def on_message(client, userdata, msg):
  #if msg.payload.decode() == "Hello world!":
  x = msg.payload.decode()
  print(x)
  loki_data = {'x'}
  print(loki_data, file=open('/home/ubuntu/mqtt/loki.txt'))
  if x == "exit":
   client.disconnect()
  
    
client = mqtt.Client()
client.connect("127.0.0.1",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()