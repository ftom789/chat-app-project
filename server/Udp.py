import socket
import datetime
import os
import base64


class Server():
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
        return data,addr

  
    def close(self):
        self.sock.close()


class ClientHandle():
    
    def __init__(self,sock,addr,clients=[]):
        self.sock=sock
        self.work=True
        self.addr=addr
        self.clients=clients
        

    def Send(self,msg):
        
        if type(msg)==str:
            size=str(len(msg.encode("utf-8")))
        else:
            size=str(len(msg))
        print(f"size is {size}")
        size="0"*(16-len(size))+size
        try:
            self.sock.send(size.encode("utf-8"))
        except:
            self.close()
            return False
        if type(msg)==str:
            size=len(msg.encode("utf-8"))
        else:
            size=len(msg)

        print(f"size is {size}")

        if type(msg)==str:
            msg=msg.encode("utf-8")
        counter=0
        sz=0
        file=open("log.txt","w")
        file.write(str(msg))
        file.close()
        while size:
            if (size>1024):
                self.sock.send(msg[:1024])
                sz+=len(msg[:1024])
                msg=msg[1024:]    
                size-=1024
                
            else:
                self.sock.send(msg)
                sz+=len(msg)
                print(f"last packet sent - {len(msg)}")
                print(f"last packet sent content - {msg}")
                size=False
            counter+=1
        print(counter)
        print(f"whole packets sent - {sz}")
        
    def Recieve(self):
        try:
            data=self.sock.recv(16)
            size=int(data.decode("utf-8"))
        except:
            self.close()
            print(data)
            print("size need to be an integer")
            return False

        if not data:
            print("nothing has benn sent")
            self.close()
            return False
        
        
        data=bytes()
        while size:
            if (size>1024):
                try:
                    data2=self.sock.recv(1024)
                    data+=data2
                    size-=len(data2)
                except:
                    self.close()
                    print("recieve does not work")

                    return False
                
            elif size>0:
                try:
                    data+=self.sock.recv(size)
                except:
                    self.close()
                    print("recieve does not work")
                    return False
                size=0
            else:
                size=0
        if not data:
            self.close()
            print("no data")
            return False
        try:
            data=data.decode("utf-8")
            pass
        finally:
            return data


    def close(self):
        print(f"{self.addr} client closed")
        self.sock.close()
        self.work=False

