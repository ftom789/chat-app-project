import tkinter
from tkinter import ttk
import io
from PIL import ImageTk
from PIL import Image

class App():

    def __init__(self,close):
        self.window=None
        self.frame=[]
        self.StringVar=[]
        self.ScrollBar=[]
        self.ListBox=[]
        self.label=[]
        self.button=[]
        self.entry=[]
        self.TreeView=[]
        self.photos=[]
        self.close=close


    def CreateWindow(self,title="client", size="300x200"):

        self.window=tkinter.Tk()
        self.window.title(title)
        self.window.geometry(size)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)
        return self.window


    def CreateFrame(self):
        frame=tkinter.Frame(self.window)
        frame.pack()
        self.frame.append(frame)
        return frame

    def CreateTextBox(self,frame,column,row,sticky,yscrollbar):
        text=tkinter.Text(frame,yscrollcommand=yscrollbar.set)
        text.grid(column=column, row=row, sticky=sticky)
        return text

    def CreateStringVar(self):
        message = tkinter.StringVar()
        self.StringVar.append(message)
        return message

    def CreateScrollBar(self,frame,side,direction,orient):
        scrollbar = ttk.Scrollbar(frame,orient=orient)
        scrollbar.grid(row=side, column=direction, sticky=tkinter.NSEW)
        
        #scrollbar.pack(side=side, fill=direction)
        self.ScrollBar.append(scrollbar)
        return scrollbar

    def CreateListBox(self,frame,height,width,yscrollbar,xscrollbar):
        ListBox=tkinter.Listbox(frame,height=height,width=width,yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)
        ListBox.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.ListBox.append(ListBox)
        return ListBox

    def CreateTreeView(self,frame,columns,yscrollbar,xscrollbar):
        tree=ttk.Treeview(frame,show="headings", columns=columns,xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set)
        tree.grid(row=0,sticky=tkinter.NSEW)
        tree.grid_rowconfigure(0, weight=1)
        tree.grid_columnconfigure(0, weight=1)  
        for item in tree["columns"]:
            tree.column(item)
            tree.heading(item, text=item)
        self.TreeView.append(tree)
        return tree

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
        entry=tkinter.Entry(frame,textvariable=stringvar,width=50)
        entry.pack()
        self.entry.append(entry)
        return entry

    def bind(self,widget,event,handler):
        widget.bind(event,handler)

    def config(self,widget,cmd):
        widget.config(command=cmd)

    def AddMessage(self,TextBox,message,tag):
        
        if type(message)==tuple and type(message[1])!=str:
            message[1]=message[1].get() 
        elif type(message)==tkinter.StringVar:
            message=message.get() 
        
        if type(message)==str:
            TextBox.insert("end", message,tag)

        elif type(message)==bytes:
            
            photo=Image.open(io.BytesIO(message))
            photo=photo.resize((128,96),Image.ANTIALIAS)
            photo=ImageTk.PhotoImage(photo)
            self.photos.append(photo)
            TextBox.image_create(tkinter.END,image=self.photos[-1],padx=tag)

        TextBox.see("end")

        self.StringVar[0].set("")
        
    def onClose(self):
        self.close()
        exit()
        self.window.quit()
        

    def mainloop(self):
        self.window.mainloop()


