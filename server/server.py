import socket
import datetime
import os
import threading

class Server():
    def __init__(self):
        self.threads = []
        self.sock = socket.socket()
        self.sock.bind(("0.0.0.0",88))
        self.sock.listen()

    def Accept(self):
        client,addr=self.sock.accept()
        return client,addr

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

    def Recieve(self,sock):
        try:
            data=sock.recv(8)
        except:
            print("client closed")
            self.removeThread(sock)
            sock.close()
            return False
        if not data:
            print("client closed")
            self.removeThread(sock)
            sock.close()
            return False
        size=int(data.decode())
        data=bytes()
        while size:
            if (size>1024):
                try:
                    data+=sock.recv(1024)
                except:
                    print("client closed")
                    self.removeThread(sock)
                    sock.close()
                    return False
                size-=1024
            else:
                try:
                    data+=sock.recv(size)
                except:
                    print("client closed")
                    self.removeThread(sock)
                    sock.close()
                    return False
                size=0
        if not data:
            print("client closed")
            self.removeThread(sock)
            sock.close()
            return False
        try:
            data=data.decode()
            pass
        finally:
            return data

    def removeThread(self,client):
        for i in self.threads:
            if client is i[1]:
                self.threads.remove(i)