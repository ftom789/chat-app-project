import tkinter
from tkinter import ttk
import io
from PIL import ImageTk
from PIL import Image,ImageFile


ImageFile.LOAD_TRUNCATED_IMAGES=True

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


    def CreateWindow(self,title="client", size="300x200",**kwargs):

        self.window=tkinter.Tk(**kwargs)
        self.window.title(title)
        self.window.geometry(size)
        self.window.resizable(True,True)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)
        return self.window


    def CreateFrame(self,**kwargs):
        frame=tkinter.Frame(self.window,**kwargs)
        
        self.frame.append(frame)
        return frame

    def pack(self,widget,**kwargs):
        widget.pack(**kwargs)

    def CreateTitleBar(self,frame,button):
        #self.window.update_idletasks()
        self.window.overrideredirect(True)
        title_bar = self.CreateFrame(**frame)
        title_bar.pack(expand=1,fill=tkinter.X)
        def get_pos(event):
            xwin = self.window.winfo_x()
            ywin = self.window.winfo_y()
            startx = event.x_root
            starty = event.y_root

            ywin = ywin - starty
            xwin = xwin - startx


            def move_window(event):
                self.window.geometry(f"{self.window.winfo_width()}x{self.window.winfo_height()}" + '+{0}+{1}'.format(event.x_root + xwin, event.y_root + ywin))
            startx = event.x_root
            starty = event.y_root
            title_bar.bind('<B1-Motion>', move_window)
        title_bar.bind('<B1-Motion>', get_pos)
        width,height=self.window.maxsize()
        maxsize_button=self.CreateButton(title_bar,text="🗖",command=lambda:self.window.geometry(f"{width}x{height}+0+0"),**button)
        close_button = self.CreateButton(title_bar,text="X",command=self.window.destroy,**button)
        close_button.pack(side=tkinter.RIGHT)
        maxsize_button.pack(side=tkinter.RIGHT)
        return title_bar,close_button

    def resize(self,widget, event):
        w,h = event.width-1, event.height-1
        print(w,h)
        widget.config(width=w, height=h)

    def CreateTextBox(self,frame,column,row,sticky,yscrollbar,**kwargs):
        text=tkinter.Text(frame,yscrollcommand=yscrollbar.set,**kwargs)
        text.grid(column=column, row=row, sticky=sticky)
        text.configure(state='disabled')
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

    def CreateLabel(self,frame,text,**kwargs):
        lblNum = tkinter.Label(frame, text=text,**kwargs)
        self.label.append(lblNum)
        return lblNum

    def CreateButton(self,frame,**kwargs):
        
        btnClick = tkinter.Button(frame,**kwargs)
        self.button.append(btnClick)
        return btnClick

    def CreateEntry(self,frame,stringvar,**kwargs):
        entry=tkinter.Entry(frame,textvariable=stringvar,**kwargs)
        self.entry.append(entry)
        return entry

    def bind(self,widget,event,handler):
        widget.bind(event,handler)

    def config(self,widget,cmd):
        widget.config(command=cmd)

    def AddMessage(self,TextBox,message,tag):
        #append message to the textBox
        TextBox.configure(state='normal') #change the state to normal means that anyone can write to the textBox
        if type(message)==tuple and type(message[1])!=str:
            message[1]=message[1].get() 
        elif type(message)==tkinter.StringVar:
            message=message.get() 
        
        if type(message)==str:
            TextBox.insert("end", message,tag)

        elif type(message)==bytes:
            
            photo=Image.open(io.BytesIO(message)) #open the photo
            photo=photo.resize((128,96),Image.ANTIALIAS) #resize the photo
            photo=ImageTk.PhotoImage(photo) #convert the photo to tkinter format
            self.photos.append(photo) #append the photo to the list of photos to save in memory
            TextBox.image_create(tkinter.END,image=self.photos[-1],padx=tag)

        TextBox.see("end") #scroll to the end of the textBox
        TextBox.configure(state='disabled') #change the state to disabled means that no one can write to the textBox
        self.StringVar[0].set("")
        
    def background(self,color):
        self.window.configure(background=color)
        for i in self.frame:
            i.configure(background=color)
        for i in self.button:
            i.configure(background=color)


    def onClose(self):
        #close the sockets and exit
        for i in self.close:
            i()
        self.window.quit()
        exit()

        
        

    def mainloop(self):
        self.window.mainloop()


