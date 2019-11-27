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

x = None
y = 1
while y is 1:
 
  def on_message(client, userdata, msg):
    #if msg.payload.decode() == "Hello world!":
    global x
    global y 
    x = msg.payload.decode()
    print(x)
    
    if x == "exit":
     client.disconnect()
    # tarkistaa onko viesti suurempi kuin kymmenen merkkiä
    if len(x) > 10:
     y = 0
    client.loop_forever()

while y is 0:
  client = mqtt.Client()
  client.connect("127.0.0.1",1883,60)

  client.on_connect = on_connect
  client.on_message = on_message

  mycursor = mydb.cursor()

  # testiy = "arduino1,2019-11-12 16:05:11.112,tulo,455,30"
  # alkusyöttö: "ard1, 2019-11-12 14:39:11.111, tulo, 455, 30"
  # my_listiin tulee viestin stringin arvot (jotka oli pilkuilla eroteltu) listana
  # [ard1], [2019-11-12 14:39:11.111], [tulo], [455], [30]

  my_list = x.split(",")
  print(my_list)
  osoite, a1_aika, a1_suunta, a1_aikaero, a1_etaisyys = my_list

  # määritetään omiin muuttujiin varmuudeksi
  #osoite = my_list[4]
  #a1_aika = my_list[3], a1_suunta = my_list[2], a1_aikaero = my_list[1], a1_etaisyys = my_list[0]
  print(a1_etaisyys, osoite)

  if osoite == "arduino1":
    sql = "INSERT INTO Arduino1 (a1_aika, a1_suunta, a1_aikaero, a1_etaisyys) VALUES (%s, %s, %s, %s)"
    val = (a1_aika, a1_suunta, a1_aikaero, a1_etaisyys)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "Arduino1 record inserted.")

  elif osoite == "arduino2":
    sql = "INSERT INTO Arduino1 (a2_aika, a2_suunta, a2_aikaero, a2_etaisyys) VALUES (%s, %s, %s, %s)"
    val = (a1_aika, a1_suunta, a1_aikaero, a1_etaisyys)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "Arduino2 record inserted.")

  elif osoite == "alue":
    sql = "INSERT INTO Arduino1 (a2_aika, a2_suunta, a2_aikaero, a2_etaisyys) VALUES (%s, %s, %s, %s)"
    val = (a1_aika, a1_suunta, a1_aikaero, a1_etaisyys)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "Arduino1 record inserted.")
    
  elif osoite == "tunnistus":
    sql = "INSERT INTO Arduino1 (a1_aika, a1_suunta, a1_aikaero, a1_etaisyys) VALUES (%s, %s, %s, %s)"
    val = (a1_aika, a1_suunta, a1_aikaero, a1_etaisyys)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "Arduino1 record inserted.")  

  else:
    y = 1

  y = 1

 # mihin muotoon viestit tulevat? oma esim: (tulee Arduino1 taululle):
 # ard1, a1_aika, a1_suunta, a1_aikaero, a1_etaisyys
 # ard1, 2019-11-12 14:39:11.111, tulo, 455, 30
 # (osoite eli mihin tauluun), aikaleima, suunta, aikaero, etäisyys (cm)