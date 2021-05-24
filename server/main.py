import threading
import re
import os
import json

clients=[]
connectedAccounts=[]


def msgServer():
    from Tcp import Server, ClientHandle
    global clients
    def clientHandle(client):
        message=True
        while message:
            message=client.Recieve()
            if not message:
                break
            try:
                message=json.loads(message)
            except :
                raise Exception("Could not convert to json")

            #message=re.search("(.*):([\s\S]*)",message)
            if message["type"]=="message":
                #message=message.group(2)
                print(f"{client.addr} {message}")
                message=json.dumps(message)
                sendMessage(client,message)
                continue
            elif message["type"]=="account":

                content=message["content"]
                print(f"username - {content['username']}, accounts - {connectedAccounts}")
                connected=False
                for account in connectedAccounts:

                    if account[1]==content['username']:
                        message={
                            "type":"account",
                            "isAccepted":False,
                            "reason":"user already connected"
                        }
                        message=json.dumps(message)
                        client.Send(message)
                        connected=True
                        break
                if connected:
                    print("connected")
                    continue
                if content["action"]=="login":
                    if  os.path.exists(f"accounts\\{content['username']}"):
                        if open(f"accounts\\{content['username']}\\password.txt","r").read()==content["password"]:
                            message={
                                "type":"account",
                                "isAccepted":True
                            }
                            connectedAccounts.append((client,content['username']))
                            message=json.dumps(message)
                            client.Send(message)
                            continue
                        else:
                            message={
                                "type":"account",
                                "isAccepted":False,
                                "reason":"password incorrect"
                            }
                            message=json.dumps(message)
                            client.Send(message)
                            continue
                    else:
                        message={
                            "type":"account",
                            "isAccepted":False,
                            "reason":"username not exist"
                        }
                        message=json.dumps(message)
                        client.Send(message)
                        continue
                elif content["action"]=="signup": 
                    if os.path.exists(f"accounts\\{content['username']}"):
                        message={
                            "type":"account",
                            "isAccepted":False,
                            "reason":"username already exist"
                        }
                        message=json.dumps(message)
                        client.Send(message)
                        continue
                    os.mkdir(f"accounts\\{content['username']}")
                    file=open(f"accounts\\{content['username']}\\password.txt", "w", encoding="UTF-8")
                    file.write(content["password"])
                    file.close()
                    message={
                        "type":"account",
                        "isAccepted":True
                    }
                    connectedAccounts.append((client,content['username']))
                    message=json.dumps(message)
                    client.Send(message)

                    

    def close(client):
        for account in connectedAccounts:
            if account[0]==client:
                connectedAccounts.remove(account)
                break

    def sendMessage(client,message):
        for i in clients:
            if i !=client and i.work:
                print(f"send to {i.addr}")
                i.Send(message)

    server=Server([close])

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