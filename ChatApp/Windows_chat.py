from time import sleep
from tkinter import *
import tkinter as tk
from mis_librerias.Centrar_Ventana import centrar_ventana
from mis_librerias.RGB import RGB
import threading

class Windows_chat:
    
    def __init__(self, user, server, first_message, opened):
        self.user = user
        self.server = server
        self.kill_thread = False
        self.first_message = first_message
        self.opened_with_message = opened        
        self.first_message_sended = False
        
        self.lock = threading.Lock()
        self.lock.acquire()
        
        self.root = Tk()
        self.root.geometry(centrar_ventana(400,400,self.root))
        self.root.title(f"Chating with {user}")
        
        self.frame = Frame(self.root)
        self.frame.config(bg = RGB((84,146,203)))
        self.frame.pack(fill = "both", expand = True)
        
        self.input_message = Text(self.frame)
        self.input_message.config(width = 40, height = 5)
        self.input_message.place(x = 10, y = 300)
        
        self.button_send = Button(self.frame, text = "Send", command = lambda: self.send_message(""))
        self.button_send.config(bg = RGB((84,146,203)))
        self.button_send.place(x = 350, y = 350)
        
        #text to show all the messages 
        self.text_show_messages = Text(self.frame)
        self.text_show_messages.config(bg = RGB((84,146,203)), width = 49, height = 15)
        self.text_show_messages.tag_config("right", justify = "right")
        self.text_show_messages.place(x = 0, y = 50)
        self.text_show_messages.insert(INSERT,f"{self.user}:{self.first_message} \n")
        
        threading.Thread(target = self.recive_message).start()
        
        self.root.bind("<Return>",self.send_message)
        
        if self.root.mainloop() == False:
            self.kill_thread = True
        self.root.mainloop()
        
    def send_message(self, event):  
        message = self.input_message.get(1.0,"end")
        self.text_show_messages.config(state = "normal")
        self.text_show_messages.insert(INSERT,(f"{message} \n"), "right")
        self.text_show_messages.config(state = "disabled")

        if self.first_message_sended == False and self.opened_with_message == False: 
            self.server.send(f"chat_to:{self.user}:{message}".encode("utf-8"))
            self.first_message_sended = True
        else: 
            self.server.send(f"private_chat:{self.user}:{message}".encode("utf-8"))
  
        self.text_show_messages.config(state = "disabled")
        self.input_message.delete("1.0","end")
  
    def recive_message(self):
        while True:
            message = self.server.recv(1024).decode("utf-8")
            message = list(message.split(":"))
            if "new_user" in message:
                pass
            else:
                self.text_show_messages.config(state = "normal")
                self.text_show_messages.insert(INSERT,f"{message[1]}:{message[2]} \n") 
                self.text_show_messages.config(state = "disabled")

            if self.kill_thread == True:
                break 
                     