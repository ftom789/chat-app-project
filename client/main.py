from gui import App
import tkinter
from client import Client
import threading
from tkinter.filedialog import askopenfilename
import re
import os
import playsound
import voicechat

def SendMessage(app, client,message_TextBox,message):
    if type(message)==tkinter.StringVar:
        message=message.get()
    mes=re.search("([\s\S]*?): ([\s\S]*)", message)
    if mes.group(1)=="message" or mes.group(1)=="image":
        app.AddMessage(message_TextBox,":tom",["Name","rtl"])
        app.AddMessage(message_TextBox,"\n","rtl")

        if mes.group(1)=="image":
            app.AddMessage(message_TextBox,bytes(mes.group(2),'latin-1'),500)
        else:
            app.AddMessage(message_TextBox,mes.group(2)+"  ","rtl")
        app.AddMessage(message_TextBox,"\n\n","rtl")
    else:
        app.AddMessage(message_TextBox,":tom",["Name","rtl"])
        app.AddMessage(message_TextBox,"\n","rtl")
        app.AddMessage(message_TextBox,"sent file"+"  ","rtl")
        app.AddMessage(message_TextBox,"\n\n","rtl")
    
    client.Send(message)

    
    
def ReceiveMessage(app, client,message_TextBox):
    message=True
    while message:
        message=client.Recieve()
        playsound.playsound("https://www.myinstants.com/media/sounds/discord-notification.mp3",block=False)
        if type(message)!=str:
            continue
        message=re.search("([\s\S]*?): ([\s\S]*)",message)
        if(message.group(1)=="message"):
            message=message.group(2)
            print(message)
            app.AddMessage(message_TextBox,"tom: ","Name")
            app.AddMessage(message_TextBox,"\n   ","")      
            app.AddMessage(message_TextBox,message,"")
            app.AddMessage(message_TextBox,"\n\n","")

        elif(message.group(1)=="image"):
            app.AddMessage(message_TextBox,"tom: ","Name")
            app.AddMessage(message_TextBox,"\n   ","")      
            message=bytes(message.group(2),'latin-1')
            app.AddMessage(message_TextBox,message,35)
            app.AddMessage(message_TextBox,"\n\n","")

        elif(message.group(1)=="file"):
            message=re.search(r"([\s\S]*?): ([\s\S]*?)\\([\s\S]*)",message.group(0))
            if not os.path.exists("files"):
                os.mkdir(os.getcwd()+r"\files")
            file=open(rf"files\{message.group(2)}","wb")
            file.write(bytes(message.group(3),"latin-1"))
            file.close()
            app.AddMessage(message_TextBox,"tom: ","Name")
            app.AddMessage(message_TextBox,"\n   ","")
            app.AddMessage(message_TextBox,f"sent file: {message.group(2)}","")
            app.AddMessage(message_TextBox,"\n\n","")




def getFile(filetypes):
    fileName = askopenfilename(title = "Select file",filetypes = filetypes)
    if fileName=="":
        return None

    file=open(fileName,"rb")
    content=file.read()
    file.close()
    return (fileName,content)

def getImage(app,client,message_TextBox):
    file=getFile((("jpeg files","*.jpg *.png"),))
    if file!=None:
        fileName,content=file
        SendMessage(app,client,message_TextBox,"image: "+content.decode('latin-1'))

def getFiles(app,client,message_TextBox):
    file=getFile((("all files","*.*"),))
    if file!=None:
        fileName,content=file
        SendMessage(app,client,message_TextBox,"file: "+fileName.split('/')[-1]+"\\"+content.decode('latin-1'))


deafen=True

def Changedeafen():
    global deafen
    deafen=not deafen
    print(deafen)

def SendVoice():
    while True:
        if not deafen:
            voicechat.Send()
def ReceiveVoice():
    while True:
        if not deafen:

            voicechat.Recieve()


first=True
def main():
    global first
    client=Client()
    client.connect()
    app=App(client.close)
    window=app.CreateWindow(size="700x550")

    msg_frame=app.CreateFrame()

    y_scrollbar=app.CreateScrollBar(msg_frame,0,1,tkinter.VERTICAL)
    #x_scrollbar=app.CreateScrollBar(msg_frame,1,0,tkinter.HORIZONTAL)
    message=app.CreateStringVar()
    message_TextBox=app.CreateTextBox(msg_frame,0,0,tkinter.NS,y_scrollbar)
    message_TextBox.tag_config('Name', foreground="red")
    message_TextBox.tag_config('rtl', justify='right')
    Button_frame=app.CreateFrame()

    entry=app.CreateEntry(Button_frame,message)
     
    SendFile_btn=app.CreateButton(Button_frame,"send File",15,lambda:getFiles(app,client,message_TextBox),"red")
    SendImg_btn=app.CreateButton(Button_frame,"send Image",15,lambda:getImage(app,client,message_TextBox),"red")
    deafen_btn=app.CreateButton(Button_frame,"deafen",15,lambda:Changedeafen(),"red")
    app.bind(entry, "<Return>", lambda args: SendMessage(app,client,message_TextBox,"message: "+message.get()) if message.get()!="" else None )
    
    y_scrollbar.configure(command=message_TextBox.yview)
    message_TextBox.configure(yscrollcommand=y_scrollbar.set)
    #x_scrollbar.configure(command=message_TextBox.xview)
    #message_TextBox.configure(xscrollcommand=x_scrollbar.set)
    app.config(y_scrollbar,message_TextBox.yview)
    
    #app.config(x_scrollbar,message_TextBox.xview)
    recvmessage=threading.Thread(target=ReceiveMessage,args=[app,client,message_TextBox])
    sendvoice=threading.Thread(target=SendVoice,args=[])
    receivevoice=threading.Thread(target=ReceiveVoice,args=[])
    recvmessage.start()
    sendvoice.start()
    receivevoice.start()
        #first=True
    first=False
    app.mainloop()



main()