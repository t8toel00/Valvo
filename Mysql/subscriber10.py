#!/usr/bin/env python3
# 9 -> 10: muuta db-syötteitä niin, että kamera kertoo suunnan arduinojen sijasta. Etäisyyksistä laskettu objektin leveys alue-taulukkoon
# Eli Arduino -> vain aika ja etäisyys, Kamera -> suunta

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

    # testiy = "arduino1,2019-11-12 12:50:11.112,tulo,455,11"
    # Tunnistus,2019-11-15 15:17:12.999,testi
    # y.split separates y string value with given separator (in this case a comma)
    # my_listiin tulee viestin stringin arvot (jotka oli pilkuilla eroteltu) listana
    # [Arduino1], [2019-11-12 14:39:11.111], [tulo], [455], [30]

    my_list = y.split(",")
    print(my_list)

    if len(my_list) == 6:
     osoite, paikalla, e_meno, e_tulo, p_meno, p_tulo = my_list

    elif len(my_list) == 4:
     osoite, aika, lev, eta = my_list

   # elif len(my_list) == 4:
   #  osoite, k_aika, ihmiset_kpl, odotettu = my_list
   # Tunnistus,2019-11-29 10:25:30.111,0,0

    elif len(my_list) == 5 or len(my_list) < 3 or len(my_list) > 6:
     print("Unexpected message/protocol. Might be too many values or too few. Values are separated with a comma , ")
     x = 1

    # määritetään omiin muuttujiin varmuudeksi esim:
    # osoite = my_list[4]
    # a1_aika = my_list[3], a1_suunta = my_list[2], a1_aikaero = my_list[1], a1_etaisyys = my_list[0]

    if osoite == "Arduino1" and len(my_list) == 4:
      sql = "INSERT INTO Arduino1 (a1_aika, a1_leveys, a1_etaisyys) VALUES (%s, %s, %s)"
      val = (aika, lev, eta)
      mycursor.execute(sql, val)
      mydb.commit()
      print(mycursor.rowcount, "Arduino1 record inserted.")
      x = 1

    elif osoite == "Arduino2" and len(my_list) == 4:
      sql = "INSERT INTO Arduino2 (a2_aika, a2_leveys, a2_etaisyys) VALUES (%s, %s, %s)"
      val = (aika, lev, eta)
      mycursor.execute(sql, val)
      mydb.commit()
      print(mycursor.rowcount, "Arduino2 record inserted.")
      x = 1

    elif osoite == "Alue" and len(my_list) == 6:
      sql = "INSERT INTO Alue (paikalla, e_meno, e_tulo, p_meno, p_tulo) VALUES (%s, %s, %s, %s, %s)"
      val = (paikalla, e_meno, e_tulo, p_meno, p_tulo)
      mycursor.execute(sql, val)
      mydb.commit()
      print(mycursor.rowcount, "Alue record inserted.")
      x = 1
      
    elif osoite == "Tunnistus" and len(my_list) == 4:
      sql = "INSERT INTO Tunnistus (k_aika, ihmiset_kpl, odotettu_kpl) VALUES (%s, %s, %s)"
     # val = (k_aika, ihmiset_kpl, odotettu)
      val = (aika, lev, eta)
      mycursor.execute(sql, val)
      mydb.commit()
      print(mycursor.rowcount, "Tunnistus record inserted.")
      x = 1  

    else:
      print("No address found")
      x = 1
