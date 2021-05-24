from Server import ClientHandleInterface
import socket
import datetime
import os
import base64


class Server(ClientHandleInterface):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("0.0.0.0",89))

        self.clients=[]

    def Send(self,message,addr):
        try:
            self.sock.sendto(message,addr)
        except:
            print("removed")
            self.clients.remove(addr)
    
    def Receive(self):
        try:    
            data,addr=self.sock.recvfrom(1024)
        except:
            return None
        
        if (addr not in self.clients):
            print(f"new client {addr}")
            self.clients.append(addr)
            return None
        return data,addr

  
    def close(self):
        self.sock.close()

