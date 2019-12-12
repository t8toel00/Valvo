#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("raspberry/+")

def on_message(client, userdata, msg):
  #if msg.payload.decode() == "Hello world!":
  #cl = client
  #ud = userdata
  #m = msg
  x = msg.payload.decode()

  print(x)
  #print(cl, ud, m, x)
  if x == "exit":
  #text_file = open("mqtt_log.txt", "w")
  #text_file.write("%s" % x)  
  #lokisyöttö tähän myös
   client.disconnect()
   #text_file.close()
    
client = mqtt.Client()
client.connect("127.0.0.1",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()