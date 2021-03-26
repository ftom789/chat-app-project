import socket
import datetime
import os

class Client():
    def __init__(self):
        self.sock = socket.socket()

    def connect(self,ip='127.0.0.1',port=88):
        self.sock.connect((ip,port))

    def Send(self,msg):
        if type(msg)==str:
            size=str(len(msg.encode("utf-8")))
        else:
            size=str(len(msg))
        size="0"*(8-len(size))+size
        self.sock.send(size.encode("utf-8"))
        size=len(msg)
        if type(msg)==str:
            msg=msg.encode("utf-8")
        while size:
            if (size>1024):
                self.sock.send(msg[:1024])
                msg=msg[1024:]    
                size-=1024
            else:
                self.sock.send(msg)
                size=0
    

    def Recieve(self):
        try:
            data=self.sock.recv(8)
            size=int(data.decode("utf-8"))
        except:
            self.close()
            return False

        if not data:
            self.close()
            return False
        
        
        data=bytes()
        while size:
            if (size>1024):
                try:
                    data+=self.sock.recv(1024)
                except:
                    self.close()
                    return False
                size-=1024
            else:
                try:
                    data+=self.sock.recv(size)
                except:
                    self.close()
                    return False
                size=0
        if not data:
            self.close()
            return False
        try:
            data=data.decode("utf-8")
            pass
        finally:
            return data

    def close(self):
        print("client closed")
        self.sock.close()
        self.work=False
        exit()