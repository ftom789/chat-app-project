from server import Server, ClientHandle
import time

def clientHandle(client):
    pass


server=Server()
while True:
    server.Accept(clientHandle)