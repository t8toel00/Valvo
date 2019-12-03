#!/usr/bin/env python3

import asyncio
import time
from time import sleep
import threading
import bluetooth
from bluetooth import *


class BaseThread(threading.Thread):

    stop_event = threading.Event()
    
    def __init__(self, callback=None, callback_args=None, *args, **kwargs):
        target = kwargs.pop('target')
        cls = self.__class__
        self.__class__.stop_event.clear()
        super(BaseThread, self).__init__(target=self.target_with_callback, *args, **kwargs)
        self.callback = callback
        self.method = target
        #self.callback_args = callback_args
    
    @classmethod
    def stop_thread(cls):
        cls.stop_event.set()

    def target_with_callback(self):
        cls = self.__class__
        while not cls.stop_event.is_set():
            self.callback_args = self.method()
            if self.callback is not None:
                self.callback(*self.callback_args)


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



def my_thread_job():
    # do any things here
    print("thread start successfully and sleep for 5 seconds")
    time.sleep(5)
    print("thread ended successfully!")

def cb(param1, param2):
    # this is run after your thread end
    print("callback function called")
    print("{} {}".format(param1, param2))

def secondJob():
    received = (1,"data here")
    return received

arduinoA = createConnection("98:D3:31:B2:B8:D4") #kim-jong-il

# example using BaseThread with callback
# thread = BaseThread(
#     name='test',
#     target=my_thread_job,
#     callback=cb,
#     callback_args=("hello", "world")
# )

thread = BaseThread(
    name='test2',
    target=secondJob,
    callback=cb)

btThread = BaseThread(
    name='bt',
    target=arduinoA.read_from_bluetooth,
    callback=cb
)

event_loop_a = asyncio.new_event_loop()

#thread.start()
btThread.start()

while True:
    x = 1
    print("no dataaa")
    time.sleep(1)