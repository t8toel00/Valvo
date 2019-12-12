#!/usr/bin/env python3
# tee viesteistä loki, muotoile ne SQL-komennoiksi ja lähetä ne tietokantaan

import paho.mqtt.client as mqtt
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="admin",
  passwd="beijing12",
  database="valvo"
)

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

mycursor = mydb.cursor()

f = "testi"
a1 = "2019-11-12 14:39:11.111"
sql = "INSERT INTO Arduino1 (a1_aika, a1_suunta, a1_aikaero, a1_etaisyys) VALUES (%s, %s, %s, %s)"
val = (a1, f, f, f)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")


client.loop_forever()

