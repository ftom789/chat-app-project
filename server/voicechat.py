from Udp import Server

server=Server()

def sendToAll(data,addr):
    for i in server.clients:
        if i != addr:
            print(f"{i} {addr}")
            server.Send(data,i)

while True:
    data=server.Receive()
    if data!=None:
        data,addr=data
        sendToAll(data,addr)