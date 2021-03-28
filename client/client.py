import socket
import datetime
import os


class Client():
    def __init__(self):
        self.sock = socket.socket()

    def connect(self,ip='192.168.0.156',port=88):
        self.sock.connect((ip,port))

    def Send(self,msg):
        if type(msg)==str:
            size=str(len(msg.encode("utf-8")))
        else:
            size=str(len(msg))
        print(f"size is {size}")
        size="0"*(16-len(size))+size
        self.sock.send(size.encode("utf-8"))
        
        if type(msg)==str:
            size=len(msg.encode("utf-8"))
        else:
            size=len(msg)
        print(f"size is {size}")
        if type(msg)==str:
            msg=msg.encode("utf-8")
        counter=0
        while size:
            if (size>1024):
                self.sock.send(msg[:1024])
                msg=msg[1024:]    
                size-=1024
            else:
                self.sock.send(msg)
                print(size)
                size=0
                
            counter+=1
        print(counter)

    def Recieve(self):
        try:
            data=self.sock.recv(16)
            size=int(data.decode("utf-8"))
            print(f"size is {size}")
        except:
            self.close()
            print(data)
            print("size need to be an integer")
            return False
#1775619
        if not data:
            print("nothing has benn sent")
            self.close()
            return False
        
        
        data=bytes()
        while size:
            if (size>1024):
                try:
                    data2=self.sock.recv(1024)
                    size-=len(data2)
                    data+=data2
                except:
                    self.close()
                    print("recieve does not work")
                    return False
                
            else:
                try:
                    data+=self.sock.recv(size)
                except:
                    self.close()
                    return False
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
        print("client closed")
        self.sock.close()
        self.work=False
    

class Udp():
    def __init__(self,addr):
        self.addr=addr
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
    def Send(self,data):
        print(len(data))
        self.sock.sendto(data,self.addr)

    def Recieve(self):
        data=self.sock.recvfrom(1024)
        return data
        
    def close(self):
        self.sock.close()
            