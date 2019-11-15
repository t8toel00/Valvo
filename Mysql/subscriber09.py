#!/usr/bin/env python3
# tee viesteistä loki, muotoile ne SQL-komennoiksi ja lähetä ne tietokantaan

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
            print(y)
            x = 0
            client.disconnect()
          else:
            print(msg.payload.decode())
            print("Viesti ei vastaa parametreja: osoite,aika,x,x,jne")
            print("esim. arduino1,2019-11-15 13:24:30.234,tietue,tietue")

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
    # alkusyöttö: "ard1, 2019-11-12 14:39:11.111, tulo, 455, 30"
    # my_listiin tulee viestin stringin arvot (jotka oli pilkuilla eroteltu) listana
    # [ard1], [2019-11-12 14:39:11.111], [tulo], [455], [30]

    my_list = y.split(",")
    print(my_list)

    if len(my_list) == 6:
     osoite, paikalla, e_meno, e_tulo, p_meno, p_tulo = my_list

    elif len(my_list) == 5:
     osoite, aika, kplsuu, ero, eta = my_list

    elif len(my_list) == 4:
     osoite, k_aika, kasvot_kpl, liipaisin = my_list

    # määritetään omiin muuttujiin varmuudeksi esim:
    # osoite = my_list[4]
    # a1_aika = my_list[3], a1_suunta = my_list[2], a1_aikaero = my_list[1], a1_etaisyys = my_list[0]

    if osoite == "arduino1" and len(my_list) == 5:
      sql = "INSERT INTO Arduino1 (a1_aika, a1_suunta, a1_aikaero, a1_etaisyys) VALUES (%s, %s, %s, %s)"
      val = (aika, kplsuu, ero, eta)
      mycursor.execute(sql, val)

      mydb.commit()

      print(mycursor.rowcount, "Arduino1 record inserted.")
      x = 1

    elif osoite == "arduino2" and len(my_list) == 5:
      sql = "INSERT INTO Arduino2 (a2_aika, a2_suunta, a2_aikaero, a2_etaisyys) VALUES (%s, %s, %s, %s)"
      val = (aika, kplsuu, ero, eta)
      mycursor.execute(sql, val)

      mydb.commit()

      print(mycursor.rowcount, "Arduino2 record inserted.")
      x = 1

    elif osoite == "alue" and len(my_list) == 6:
      sql = "INSERT INTO Alue (paikalla, e_meno, e_tulo, p_meno, p_tulo) VALUES (%s, %s, %s, %s, %s)"
      val = (paikalla, e_meno, e_tulo, p_meno, p_tulo)
      mycursor.execute(sql, val)

      mydb.commit()

      print(mycursor.rowcount, "Alue record inserted.")
      x = 1
      
    elif osoite == "tunnistus" and len(my_list) == 4:
      sql = "INSERT INTO Tunnistus (k_aika, kasvot_kpl, liipaisin) VALUES (%s, %s, %s)"
      val = (k_aika, kasvot_kpl, liipaisin)
      mycursor.execute(sql, val)

      mydb.commit()

      print(mycursor.rowcount, "Tunnistus record inserted.")
      x = 1  

    else:
      print("Osoitetta ei loytynyt")
      x = 1

  # mihin muotoon viestit tulevat? oma esim: (tulee Arduino1 taululle):
  # ard1, a1_aika, a1_suunta, a1_aikaero, a1_etaisyys
  # ard1, 2019-11-12 14:39:11.111, tulo, 455, 30
  # (osoite eli mihin tauluun), aikaleima, suunta, aikaero, etäisyys (cm)
