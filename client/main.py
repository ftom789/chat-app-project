from gui import App
import tkinter
from client import Client
import threading
from tkinter.filedialog import askopenfilename
import re
import os
import playsound
import voicechat
import json



def SendMessage(app, client,message_TextBox,message,name):
    if type(message)==tkinter.StringVar:
        message=message.get()
    
    #mes=re.search("([\s\S]*?) ([\s\S]*?): ([\s\S]*)", message)
    if message["type"]=="text" or message["type"]=="image":
        app.AddMessage(message_TextBox,f":{name}",["Name","rtl"])
        app.AddMessage(message_TextBox,"\n","rtl")
        if message["type"]=="image":
            app.AddMessage(message_TextBox,bytes(message["content"],'latin-1'),500)
        else:
            app.AddMessage(message_TextBox,message["content"]+"  ",["rtl","message"])
        app.AddMessage(message_TextBox,"\n\n","rtl")
    else:
        app.AddMessage(message_TextBox,f":{name}",["Name","rtl"])
        app.AddMessage(message_TextBox,"\n","rtl")
        app.AddMessage(message_TextBox,f"sent file: {message['fileName']}"+"  ",["rtl","message"])
        app.AddMessage(message_TextBox,"\n\n","rtl")
        
    message["name"]=name
    message={
        "type": "message", #message or account
        "content": message
    }
    
    message=json.dumps(message)
    #print(message)
    client.Send(message)

    
    
def ReceiveMessage(app, client,message_TextBox):
    message=True
    while message:
        message=client.Recieve()
        if not message:
            message=False
            break
        if type(message)!=str:
            continue
        playsound.playsound("https://www.myinstants.com/media/sounds/discord-notification.mp3",block=False) #play sound if recieved message
        message=json.loads(message)
        if message["type"]=="message":
            message=message["content"]
        #check the message
            if(message["type"]=="text"):
                #print(message)
                app.AddMessage(message_TextBox,f"{message['name']}: ","Name")
                app.AddMessage(message_TextBox,"\n   ","")      
                app.AddMessage(message_TextBox,message["content"],"message")
                app.AddMessage(message_TextBox,"\n\n","")

            elif(message["type"]=="image"):
                app.AddMessage(message_TextBox,f"{message['name']}: ","Name")
                app.AddMessage(message_TextBox,"\n   ","")      
                message=bytes(message["content"],'latin-1')
                app.AddMessage(message_TextBox,message,35)
                app.AddMessage(message_TextBox,"\n\n","")

            elif(message["type"]=="file"):
                #message=re.search(r"([\s\S]*?) ([\s\S]*?): ([\s\S]*?)\\([\s\S]*)",message.group(0))
                if not os.path.exists("files"):
                    os.mkdir(os.getcwd()+r"\files")
                file=open(rf"files\{message['fileName'].split('/')[-1]}","wb")
                file.write(bytes(message['content'],"latin-1"))
                file.close()
                app.AddMessage(message_TextBox,f"{message['name']}: ","Name")
                app.AddMessage(message_TextBox,"\n   ","")
                app.AddMessage(message_TextBox,f"sent file: {message['fileName']}","message")
                app.AddMessage(message_TextBox,"\n\n","")




def getFile(filetypes):
    fileName = askopenfilename(title = "Select file",filetypes = filetypes) #open the file system and asking the user to selecrt a file a file
    if fileName=="": #if the user didn't select a file return None
        return None

    file=open(fileName,"rb")
    content=file.read() #read the file bytes
    file.close()
    return (fileName,content)

def getImage(app,client,message_TextBox,name):
    file=getFile((("jpeg files","*.jpg *.png"),))
    if file!=None:
        fileName,content=file
        message={
        "type": "image", #text, image or file  
        "content": content.decode('latin-1')
        }
        SendMessage(app,client,message_TextBox,message,name) #sending image to the server and show the image in the textBox

def getFiles(app,client,message_TextBox,name):
    file=getFile((("all files","*.*"),))
    if file!=None:
        fileName,content=file
        message={
        "type": "file", #text, image or file  
        "fileName": fileName,
        "content": content.decode("latin-1")
        }
        SendMessage(app,client,message_TextBox,message,name) #sending file to the server


deafen=True

def Changedeafen(btn,img):
    global deafen
    global sendvoice
    global receivevoice
    deafen=not deafen
    if deafen:
        btn.configure(image=img[0])
    else:
        btn.configure(image=img[1])
    #print(deafen)
    if not deafen:
        sendvoice.start()
        receivevoice.start()
    else:
        sendvoice=threading.Thread(target=SendVoice,args=[])
        receivevoice=threading.Thread(target=ReceiveVoice,args=[])
def SendVoice():
    while not deafen:
        voicechat.Send()
        
def ReceiveVoice():
    while not deafen:
        voicechat.Recieve()

sendvoice=threading.Thread(target=SendVoice,args=[])
receivevoice=threading.Thread(target=ReceiveVoice,args=[])

def close():
    global deafen
    deafen=False

def main(client,username):
    global first
    
    voicechat.connect()
    app=App([close,client.close,voicechat.Close])
    window=app.CreateWindow(size="700x550+200+200")
    #window.overrideredirect(True)
    #
    #title_bar,close_button = app.CreateTitleBar({"bg":'white', "relief":'raised', "bd":2},{"fg":"white","width":10})
    
    
    
    msg_frame=app.CreateFrame()
    msg_frame.pack(expand=True)

    y_scrollbar=app.CreateScrollBar(msg_frame,0,1,tkinter.VERTICAL)
    #y_scrollbar.configure(background="#292b2f")
    #x_scrollbar=app.CreateScrollBar(msg_frame,1,0,tkinter.HORIZONTAL)
    message=app.CreateStringVar()
    message_TextBox=app.CreateTextBox(msg_frame,0,0,tkinter.NS,y_scrollbar,bg="#36393f")
    message_TextBox.tag_config('Name', foreground="red") #tag for name
    message_TextBox.tag_config('rtl', justify='right') 
    message_TextBox.tag_config('message', foreground="#dcddde") 
    #message_TextBox.bind('<Configure>',lambda event: app.resize(message_TextBox,event))
    Button_frame=app.CreateFrame()
    Button_frame.pack(expand=True)

    entry=app.CreateEntry(Button_frame,message)
    entry.pack()
    entry.configure(background="#36393f",fg="#dcddde")

    imageImg=tkinter.PhotoImage(file="resource\\image.png")
    fileImg=tkinter.PhotoImage(file="resource\\file.png")
    SendFile_btn=app.CreateButton(Button_frame,text="send File",width=48,command=lambda:getFiles(app,client,message_TextBox,username),image=fileImg,bd=0)
    SendFile_btn.pack(padx=25, pady=20,side=tkinter.LEFT)
    SendImg_btn=app.CreateButton(Button_frame,text="send Image",width=48,command=lambda:getImage(app,client,message_TextBox,username),image=imageImg,bd=0)
    SendImg_btn.pack(padx=25, pady=20,side=tkinter.LEFT)
    deafenImg=tkinter.PhotoImage(file="resource\\deafen.png")
    deafenOffImg=tkinter.PhotoImage(file="resource\\deafen-off.png")
    deafen_btn=app.CreateButton(Button_frame,text="",width=48,image=deafenImg,bd=0)
    deafen_btn.pack(padx=25, pady=20,side=tkinter.LEFT)
    


    deafen_btn.configure(command=lambda:Changedeafen(deafen_btn,[deafenImg,deafenOffImg]))
    app.bind(entry, "<Return>", lambda args: SendMessage(app,client,message_TextBox,{"type":"text", "content":message.get()},username) if message.get()!="" else None )
    
    y_scrollbar.configure(command=message_TextBox.yview)
    message_TextBox.configure(yscrollcommand=y_scrollbar.set)
    #x_scrollbar.configure(command=message_TextBox.xview)
    #message_TextBox.configure(xscrollcommand=x_scrollbar.set)
    app.config(y_scrollbar,message_TextBox.yview)
    app.background("#292b2f")
    #title_bar.configure(bg="#202225")
    #app.config(x_scrollbar,message_TextBox.xview)
    recvmessage=threading.Thread(target=ReceiveMessage,args=[app,client,message_TextBox])
    recvmessage.start()

    app.mainloop()


