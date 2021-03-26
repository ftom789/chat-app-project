from server import Server, ClientHandle
import time

clients=[]

def clientHandle(client):
    while True:

        message=client.Recieve()
        if not message:
            break
        print(f"{client.addr} {message}")
        sendMessage(client,message)

def sendMessage(client,message):
    for i in clients:
        if i !=client:
            print(f"send to {i.addr}")
            i.Send(message)

server=Server()
while True:
    clients=server.Accept(clientHandle)


    