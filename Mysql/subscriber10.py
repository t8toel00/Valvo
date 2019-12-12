#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import mysql.connector
import time

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="admin",
  passwd="beijing12",
  database="valvo"
)

z = 1
while z == 1:

  y = 0
  x = 1

  while x == 1:
      
      def on_connect(client, userdata, flags, rc):
          print("Connected with result code "+str(rc))
          client.subscribe("raspberry/+")

      def on_message(client, userdata, msg):
          global x
          global y
          if len(msg.payload.decode()) > 10: 
            y = msg.payload.decode()
            print('Msg received: ', y)
            x = 0
            client.disconnect()
          else:
            print(msg.payload.decode())
            print("Message doesn't contain matching parameters: osoite,aika,x,x,jne")
            print("eg. arduino1,2019-11-15 13:24:30.234,tietue,tietue")

      def closeMqtt():
          client.disconnect()

      client = mqtt.Client()
      client.connect("127.0.0.1",1883,60)
      client.on_connect = on_connect
      client.on_message = on_message
    
      client.loop_forever()


  while x == 0:
    
    mycursor = mydb.cursor()

    # y.split separates y string value with given separator (in this case a comma)
    # my_listiin tulee viestin stringin arvot (jotka oli pilkuilla eroteltu) listana

    my_list = y.split(",")
    print(my_list)
    print("Checking for address ") # Jää tähän looppiin

    if len(my_list) == 7:
     osoite, aika, kam_lkm, ant_lkm, sisa_lkm, ulo_lkm, leveys = my_list

    if len(my_list) != 7:
     print("Unexpected message/protocol. Might be too many values or too few. Values are separated with a comma , ")
     print("osoite, aika, kamera lkm, sensori lkm, sis lkm, ulos lkm, leveys")
     x = 1

   # Aika, kamera lkm, sensori lkm, sis lkm, ulos lkm, leveys

    # määritetään omiin muuttujiin varmuudeksi esim:
    # osoite = my_list[4]
    # a1_aika = my_list[3], a1_suunta = my_list[2], a1_aikaero = my_list[1], a1_etaisyys = my_list[0]
      
    elif osoite == "Tunnistus":
      sql = "INSERT INTO Tunnistus (k_aika, ihmiset_kpl, odotettu_kpl, sisa_lkm, ulos_lkm, lev) VALUES (%s, %s, %s, %s, %s, %s)"
      val = (aika, kam_lkm, ant_lkm, sisa_lkm, ulo_lkm, leveys)
      mycursor.execute(sql, val)
      mydb.commit()
      print(mycursor.rowcount, "Tunnistus record inserted.")
      x = 1  

    else:
      print("Error. Something unexpected happened.")
      x = 1
