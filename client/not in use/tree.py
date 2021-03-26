import tkinter as tk
from PIL import ImageTk
from PIL import Image

def sendMessageClick( event, textField):
		print(textField.get())
		textField.delete(0, "end") #clears textField

root = tk.Tk()
root.minsize(600,400)

mainFrame = tk.Frame(root)
mainFrame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


#ChatField
chat = tk.Text(mainFrame)
chat.tag_config('Name', foreground="red")
chat.tag_config('rtl', justify='right')
chat.grid(column=0, row=0, sticky=tk.N + tk.S + tk.W + tk.E)
chat.insert("end","ftom789:","Name")

photo=Image.open(r"C:\Users\ftom7\OneDrive\Pictures\mylogo.png")
photo=photo.resize((70,70))
photo=ImageTk.PhotoImage(photo)
chat.image_create(tk.END,image=photo,padx=400)
chat.insert("end","\n\n")
chat.insert("end","ftom789:","Name")

chat.image_create(tk.END,image=photo)
chat.insert("end","\n\n")

chat.insert("end","ftom789:","Name")



#TextFieldToSend
textField = tk.Entry(mainFrame)
textField.grid(column=0, row=1, sticky=tk.N + tk.S + tk.W + tk.E)

#SendMessageButton
buttonSend = tk.Button(mainFrame)
buttonSend["text"] = "Send Message"
buttonSend.grid(column=0, row=2, sticky=tk.N + tk.S + tk.W + tk.E)
buttonSend.bind("<Button-1>", lambda event:sendMessageClick(None,textField))


#usersPanel
usersPanel= tk.Listbox(mainFrame)
usersPanel.insert(1, "ALL")
usersPanel.grid(column=2, row=0, sticky=tk.N + tk.S + tk.W + tk.E)

#ExitButton
buttonExit = tk.Button(mainFrame)
buttonExit["text"] = "Exit"
buttonExit["background"] = "gray"
buttonExit.grid(column=2, row=2, sticky=tk.N + tk.S + tk.W + tk.E)

root.mainloop()