import socket
import datetime
import os
import threading



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
        clnt=ClientHandle(client,addr,self.threads)
        thread=threading.Thread(target=clientFunc,args=[clnt])
        thread.start()
        self.clients.append(clnt)
        self.threads.append((thread,clnt))
        return self.clients

    def close(self):
        self.sock.close()
       

    
    

class ClientHandle():
    
    def __init__(self,sock,addr,threads=[]):
        self.sock=sock
        self.work=True
        self.threads=threads
        self.addr=addr
        

    def Send(self,msg):
        
        if type(msg)==str:
            size=str(len(msg.encode("utf-8")))
        else:
            size=str(len(msg))
        size="0"*(8-len(size))+size
        try:
            self.sock.send(size.encode("utf-8"))
        except:
            self.close()
            return False
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

    def removeThread(self):
        for i in self.threads:
            if self is i[1]:
                self.threads.remove(i)
                    


    def close(self):
        print("client closed")
        self.sock.close()
        self.work=False
        self.removeThread()
