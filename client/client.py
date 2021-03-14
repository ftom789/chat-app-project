import socket
import datetime
import os

class client():
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect(('127.0.0.1',88))
        
    def Send(self,msg):
        size=str(len(msg))
        size="0"*(8-len(size))+size
        self.sock.send(size.encode())
        size=len(msg)
        if type(msg)==str:
            msg=msg.encode()
        while size:
            if (size>1024):
                self.sock.send(msg[:1024])
                msg=msg[1024:]    
                size-=1024
            else:
                self.sock.send(msg)
                size=0
