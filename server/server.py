import socket
import datetime
import os
import threading
import base64

BUFFER_SIZE = 5120

class Server():
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(("0.0.0.0",88))
        self.sock.listen()
        self.threads=[]
        self.clients=[]
        

    def Accept(self,clientFunc):
        client,addr=self.sock.accept()
        print(f"new client {addr}")
        clnt=ClientHandle(client,addr,self.threads,self.clients)
        thread=threading.Thread(target=clientFunc,args=[clnt])
        thread.start()
        self.clients.append(clnt)
        self.threads.append((thread,clnt))
        return self.clients

    def close(self):
        self.sock.close()
       

    
    

class ClientHandle():
    
    def __init__(self,sock,addr,threads=[],clients=[]):
        self.sock=sock
        self.work=True
        self.threads=threads
        self.addr=addr
        self.clients=clients
        pass

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
            if (size>BUFFER_SIZE):
                self.sock.send(msg[:BUFFER_SIZE])
                sz+=len(msg[:BUFFER_SIZE])
                msg=msg[BUFFER_SIZE:]    
                size-=BUFFER_SIZE
                
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
                    data2=self.sock.recv(BUFFER_SIZE)
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

    def removeThread(self):
        for i in self.threads:
            if self == i[1]:
                self.threads.remove(i)
        for i in self.clients:
            if self == i:
                self.clients.remove(i)
                    


    def close(self):
        print(f"{self.addr} client closed")
        self.sock.close()
        self.work=False
        self.removeThread()
