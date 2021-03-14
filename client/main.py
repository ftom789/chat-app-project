from socket import close
import tkinter
import client


class App():

    def __init__(self):
        self.window=None
        self.frame=[]
        self.StringVar=[]
        self.ScrollBar=[]
        self.ListBox=[]
        self.label=[]
        self.button=[]
        self.entry=[]
        self.sock=client.Client("127.0.0.1",2222)
        self.sock.Connect()


    def CreateWindow(self,title="client", size="300x200"):

        self.window=tkinter.Tk()
        self.window.title(title)
        self.window.geometry(size)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)


    def CreateFrame(self):
        frame=tkinter.Frame(self.window)
        frame.pack()
        self.frame.append(frame)
        return frame

    def CreateStringVar(self):
        message = tkinter.StringVar()
        self.StringVar.append(message)
        return message

    def CreateScrollBar(self,frame,side,direction,orient):
        scrollbar = tkinter.Scrollbar(frame,orient=orient)
        scrollbar.pack(side=side, fill=direction)
        self.ScrollBar.append(scrollbar)
        return scrollbar

    def CreateListBox(self,frame,height,width,yscrollbar,xscrollbar):
        ListBox=tkinter.Listbox(frame,height=height,width=width,yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)
        ListBox.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.ListBox.append(ListBox)
        return ListBox

    def CreateLabel(self,text,pady):
        lblNum = tkinter.Label(self.window, text=text)
        lblNum.pack(pady=pady)
        self.label.append(lblNum)
        return lblNum

    def CreateButton(self,frame,text,width,cmd,color):
        btnClick = tkinter.Button(frame, text = text, width = width, command=cmd, bg=color)
        btnClick.pack(padx=10, pady=20,side=tkinter.LEFT)
        self.button.append(btnClick)
        return btnClick

    def CreateEntry(self,frame,stringvar):
        entry=tkinter.Entry(frame,textvariable=stringvar)
        entry.pack()
        self.entry.append(entry)
        return entry

    def bind(self,widget,event,handler):
        widget.bind(event,handler)

    def config(self,widget,cmd):
        widget.config(command=cmd)

    def send(self,code,ListBox,message):
        if type(message)!=str:
            message=message.get()

        if code==4:
            self.onClose()

        self.sock.SendToServer(self.sock.Message(code,message))
        recieve=self.sock.RecieveMessage()
        
        if code==3:
            ListBox.insert(tkinter.END, ("File saved - "+message.split('\\')[-1]))

            
            
        ListBox.insert(tkinter.END,recieve)
        self.StringVar[0].set("")
        
    def onClose(self):
        self.sock.SendToServer(self.sock.Message(4,"quit"))
        self.sock.Close()
        self.window.quit()
        exit()

    def mainloop(self):
        self.window.mainloop()


def main():

    app=App()
    app.CreateWindow(size="600x550")

    msg_frame=app.CreateFrame()

    y_scrollbar=app.CreateScrollBar(msg_frame,tkinter.RIGHT,tkinter.Y,"vertical")
    x_scrollbar=app.CreateScrollBar(msg_frame,tkinter.BOTTOM,tkinter.X,"horizontal")
    message=app.CreateStringVar()
    message_ListBox=app.CreateListBox(msg_frame,20,80,y_scrollbar,x_scrollbar)

    Button_frame=app.CreateFrame()

    entry=app.CreateEntry(Button_frame,message)
    
    app.bind(entry, "<Return>", lambda event: app.send(1,message_ListBox,message))
    
    app.CreateButton(Button_frame,"send",10,lambda : app.send(1,message_ListBox,message), "red")
    app.CreateButton(Button_frame,"get list of files",10,lambda : app.send(2,message_ListBox,message),"light blue")
    app.CreateButton(Button_frame,"download files",10,lambda : app.send(3,message_ListBox,message),"green")
    app.CreateButton(Button_frame,"quit",10,lambda : app.send(4,message_ListBox,"quit"),"white")
    app.config(y_scrollbar,message_ListBox.yview)
    app.config(x_scrollbar,message_ListBox.xview)




    app.mainloop()

main()