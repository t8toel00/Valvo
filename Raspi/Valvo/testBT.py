    
#!/usr/bin/env python3
import bluetooth


def receiveMessages():
  server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  
  port = 1
  server_sock.bind(("",port))
  server_sock.listen(1)
  
  client_sock,address = server_sock.accept()
  print ("Accepted connection from " + str(address))
  
  data = client_sock.recv(1024)
  print ("received [%s]" % data)
  
  client_sock.close()
  server_sock.close()






  
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
            self._socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self._socket.connect((self.address, self.port))
            return True
        except bluetooth.BluetoothError as error:
            if self._socket is not None:
                self._socket.close()
                self._socket = None
            if suppress_exceptions:
                print(error)
                return False
            else:
                print(error)
                # raise BluetoothException(error.message)
        return False 
    
    def change_port(self, new_port):
        self.port = new_port
    
    def sendMessageTo(self,targetBluetoothMacAddress):
        self.sock.send("hello!!")
        self.sock.close()

    def listenToBT(self,BTMacAddress):
        self.sock.listen(1)
        self.data = sock.recv(1024)
        return self.data