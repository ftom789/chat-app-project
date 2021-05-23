import socket
import datetime
import os

BUFFER_SIZE = 5120

class Client():
    def __init__(self):
        self.sock = socket.socket() #create socket

    def connect(self,ip='192.168.0.156',port=88):
        self.sock.connect((ip,port)) #connect to the server

    def Send(self,msg):
        #get the size of the message
        if type(msg)==str:
            size=str(len(msg.encode("utf-8"))) 
        else:
            size=str(len(msg))
        print(f"size is {size}")
        size="0"*(16-len(size))+size
        self.sock.send(size.encode("utf-8")) #send the size of the message to the server. the server will be ready for that amount of data
        
        if type(msg)==str:
            size=len(msg.encode("utf-8"))
        else:
            size=len(msg)
        print(f"size is {size}")
        if type(msg)==str:
            msg=msg.encode("utf-8")
        counter=0
        while size:
            if (size>BUFFER_SIZE):
                self.sock.send(msg[:BUFFER_SIZE])
                msg=msg[BUFFER_SIZE:]    
                size-=BUFFER_SIZE
            else:
                self.sock.send(msg)
                print(size)
                size=0
                
            counter+=1
        print(counter)

    def Recieve(self):
        
        try:
            data=self.sock.recv(16)
            size=int(data.decode("utf-8")) #recieve the size of data
            print(f"size is {size}")
        except:
            self.close()
            print("size need to be an integer")
            return False

        if not data:
            print("nothing has benn sent")
            self.close()
            return False
        
        
        data=bytes()
        while size:
            if (size>BUFFER_SIZE):
                try:
                    data2=self.sock.recv(BUFFER_SIZE) #collect the data
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
        if not data: #if the message was empty it means that the other side closed the connection
            self.close()
            print("no data")
            return False
        try:
            data=data.decode("utf-8") #if it is string we will decode the message
            pass
        finally:
            return data #finally we will return the message we got

    def close(self):
        print("client closed") #close the client
        self.sock.close()
        self.work=False
    

class Udp():
    def __init__(self,addr):
        self.addr=addr
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #create socket object
        
    def Send(self,data):
        self.sock.sendto(data,self.addr) #send to the address the data

    def Recieve(self):
        data=self.sock.recvfrom(BUFFER_SIZE) #recieve data
        return data
        
    def close(self):
        self.sock.close() #close the client
            