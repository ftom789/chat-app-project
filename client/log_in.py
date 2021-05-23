from gui import App
import tkinter
from client import Client
import json
import main

client=Client()
client.connect()

def login(username,password):
    message={
        "type":"account",
        "content":{
            "action":"login",
            "username":username,
            "password":password
        }
    }
    message=json.dumps(message)
    client.Send(message)
    message=client.Recieve()
    message=json.loads(message)
    if message["isAccepted"]==True:
        app.onClose()
        main.main(client,username)
        
        
    
def signup(username,password):
    message={
        "type":"account",
        "content":{
            "action":"signup",
            "username":username,
            "password":password
        }
    }
    message=json.dumps(message)
    client.Send(message)
    message=client.Recieve()
    message=json.loads(message)
    if message["isAccepted"]==True:
        app.onClose()
        main.main(client,username)


app=App([])
app.CreateWindow()
loging=app.CreateFrame()
loging.pack()
user_label=app.CreateLabel(loging,"Enter username")
pass_label=app.CreateLabel(loging,"Enter password")
user_label.grid(row=1,column=0)
pass_label.grid(row=2,column=0)
stringvar_user=app.CreateStringVar()
stringvar_pass=app.CreateStringVar()
user_entry= app.CreateEntry(loging,stringvar_user)
user_entry.grid(row=1,column=1)  
pass_entry= app.CreateEntry(loging,stringvar_pass)
pass_entry.grid(row=2,column=1)  
login_button=app.CreateButton(loging, text="Log in", bg="cyan")
signup_button=app.CreateButton(loging, text= "sign up", bg= "yellow")
login_button.configure(command=lambda:login(stringvar_user.get(),stringvar_pass.get()))
signup_button.configure(command=lambda:signup(stringvar_user.get(),stringvar_pass.get()))
login_button.grid(row=3,column=0)
signup_button.grid(row=3,column=1)







app.mainloop()


