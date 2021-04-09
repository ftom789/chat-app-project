import threading
import re
import os

clients=[]

def msgServer():
    from server import Server, ClientHandle
    global clients
    def clientHandle(client):
        message=True
        while message:

            message=client.Recieve()
            if not message:
                break
            message=re.search("(.*):([\s\S]*)",message)
            if message.group(1)=="mes":
                message=message.group(2)
                print(f"{client.addr} {message}")
                sendMessage(client,message)
            elif message.group(1)=="acc":
                action,username,password=re.search("(.*):([\s\S]*)//([\s\S]*)",message).groups() 
                if action=="login":
                    if  os.path.exists(f"accounts\\{username}"):
                        if open(f"accounts\\{username}\\password.txt","r").read()==password:
                            client.Send("accepted")
                        else:
                            client.Send("not accepted:password is not correct")
                    else:
                        client.Send("not accepted:username not exist")
                elif action=="signup": 



    def sendMessage(client,message):
        for i in clients:
            if i !=client and i.work:
                print(f"send to {i.addr}")
                i.Send(message)

    server=Server()

    while True:
        clients=server.Accept(clientHandle)
        print(clients)


def voiceServer():
    from Udp import Server

    server=Server()

    def sendToAll(data,addr):
        for i in server.clients:
            if i != addr:
                #print(f"{i} {addr}")
                server.Send(data,i)

    def RemoveAFK():
        print(f"udp{server.clients} tcp{clients}")
        for i in server.clients:
            found=False
            for j in clients:
                if i[0]==j.addr[0]:
                    found=True
                    break
            if not found:
                server.clients.remove(i)
                print(f"udp {i}")



    while True:
        RemoveAFK()
        data=server.Receive()
        if data!=None:
            data,addr=data
            sendToAll(data,addr)
            


msg=threading.Thread(target=msgServer)
voice=threading.Thread(target=voiceServer)
msg.start()
voice.start()