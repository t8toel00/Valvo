    
#!/usr/bin/env python3
import bluetooth
from bluetooth import *
import subprocess


def lookUpNearbyBluetoothDevices():
    nearby_devices = bluetooth.discover_devices()
    if len(nearby_devices) !=0:
        print("Devices found: " + chr(10))
        opt = 0
        devicelist = {}
        for bdaddr in nearby_devices:
            opt = opt + 1
            devicelist[str(opt)] = bdaddr
            print(str(opt) + ") " + str(bluetooth.lookup_name( bdaddr )) + " [" + str(bdaddr) + "]") 
            #print([_ for _ in find_service(address=bdaddr) if 'RFCOMM' in _['protocol'] ])
            #print([_ for _ in find_service(address=bdaddr) ])  
    else:
        print("No devices found")
        return ""
    
    return devicelist[input("Select a device: ")]

class BTConn():
    def __init__(self):
        self.port = 1
        #self.address = None

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
    
    def change_port(self, new_port):
        self.port = new_port
    
    def sendMessageTo(self,mesg):
        self.sock.send("hello!!")
    
    def close(self):
        self.sock.close()

    def listenToBT(self):
        #self.sock.bind(("",2))
        #self.sock.listen(1)
        try:
            self.data = self.sock.recv(512)
            return self.data
        except bluetooth.bluetoothError as error:
            return error
        
        
            

class BTServerConn():

    def __init__(self):
        self.server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.port = 2

    def bind(self):
        self.server_sock.bind(("", self.port))
        self.server_sock.listen(1)
        self.client_sock,address = self.server_sock.accept()
    
    def receive(self):
        data = self.client_sock.recv(1024)
        return data
        

    def close(self):
        self.sock.shutdown()
        self.sock.close()
        