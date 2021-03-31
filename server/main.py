import threading


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
            print(f"{client.addr} {message}")
            sendMessage(client,message)

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