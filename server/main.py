from server import Server, ClientHandle

clients=[]

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


    