from gui import App
import tkinter

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
login_butten=app.CreateButton(loging, text="Log in", bg= "cyan")
signup_butten=app.CreateButton(loging, text= "sign up", bg= "yellow")
login_butten.grid(row=3,column=0)
signup_butten.grid(row=3,column=1)





app.mainloop()

