#!/usr/bin/env python3

import bluetooth
import BTAsync
from BTAsync import *
from time import sleep

def handle_read(conn):
    print("Received data:", str(btdata))
    time.sleep(.500)


def createConnection(adr):

    # Create new instance of BTConn() class and search for devices.
    connection = BTConn()
    # Get the MAC address of a found device:
    #adr = lookUpNearbyBluetoothDevices()
    
    print("Connecting to device " + adr)
    # Try to connect and try again if not successful:
    attempt = 0
    connected = False
    while connected == False:
        
        while connection.connect(address = adr) == False and attempt < 5:
            print("Failed to connect. Retrying...")
            attempt = attempt + 1
            time.sleep(.500)

        if attempt < 5:
            print("Connection successful to device " + adr)
            connected == True
            return connection
        else:
            #print("Unable to connect to '" + adr + "'. Please choose one manually.")
            #print("Now scanning for nearby devices...")
            #adr = lookUpNearbyBluetoothDevices()
            attempt = 0


arduinoA = createConnection("98:D3:31:B2:B9:4C") #kim-jong-ung
arduinoA.handle_read = handle_read

while True:
    print("Nothing to see here")

