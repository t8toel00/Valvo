#!/usr/bin/env python3

from threading import Thread
import bluetooth
from bluetooth import *
import time
from time import sleep

def foo(bar):
    print('hello {0}'.format(bar))
    return "foo"


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

class BTConn():

    def __init__(self):
        self.port = 1

    def connect(self, address=None, suppress_exceptions=False):
        """
        Returns True if a connection is successfully made, False otherwise.

        `address` is bluetooth address, that must be set previously or given as a keyword argument.

        If `suppress_exceptions` is set to `True` exceptions thrown by the
        bluetooth library will be suppressed, and the function will return false.

        If there is a current connection it is closed before an attempt to connect is made.
        """

        if address is not None:
            self.address = address

        if self.address is None:
            return False

        #self.close()

        try:
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.connect((self.address, self.port))
            return True
        except bluetooth.BluetoothError as error:
            if str(error) == "(111, 'Connection refused')":
                #self.pin = str(input("Please enter a pin for the device: "))
                print("Connection refused, has the device been paired?")
            if self.sock is not None:
                self.sock.close()
                self.sock = None
            if suppress_exceptions:
                print(error)
                return False
            else:
                print(error)
                # raise BluetoothException(error.message)
        return False 

    def read_from_bluetooth(self):
        while True:
            try:
                data = self.sock.recv(1024)
                return self.address, data
            except:
                print("error")

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
    def reset(self):
        self._return = None

def test(dat):
    print("dataa:", dat)

#arduinoA = createConnection("98:D3:31:B2:B9:4C") #kim-jong-ung
arduinoA = createConnection("98:D3:31:B2:B8:D4") #kim-jong-il
#twrv = ThreadWithReturnValue(target=foo, args=('world!',))

thrPollBT = ThreadWithReturnValue(target=arduinoA.read_from_bluetooth)
thrPollBT.start()
arduinoA.class_callback = test

while True:
    print("no data")
    print(thrPollBT.join())
    #thrPollBT.reset()
    

#twrv.start()
#print(twrv.join())   # prints foo