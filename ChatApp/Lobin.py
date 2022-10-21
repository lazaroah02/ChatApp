from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from mis_librerias.Centrar_Ventana import centrar_ventana 
from mis_librerias.RGB import RGB
import socket, threading, Windows_chat

class Lobin:
    def __init__(self):
        self.threading = threading
        self.kill_thread = False
        self.server = socket.socket()
        self.list_of_users = []
        self.top_level_opened = False
        self.thread_get_message = None
        
        self.lock = threading.Lock()

        self.root = Tk()
        self.root.geometry(centrar_ventana(400,400,self.root))
        self.root.title("ChatApp")
        
        self.frame = Frame(self.root)
        self.frame.config(bg = RGB((84,146,203)))
        self.frame.pack(fill = "both", expand = True)
        
        #Entry to input the host address
        self.label_host_address = Label(self.frame, text = "Host Address")
        self.label_host_address.config(bg = RGB((84,146,203)))
        self.label_host_address.place(x = 200, y = 30)
        
        self.input_host_address = Entry(self.frame)
        self.input_host_address.insert(INSERT,"localhost:8888")
        self.input_host_address.place(x = 200, y = 50)
        
        self.button_connect_server = Button(self.frame, text = "Connect", command = lambda: self.logic_button_connect_server("") )
        self.button_connect_server.config(bg = RGB((84,146,203)), width = 8, height = 2)
        self.button_connect_server.place(x = 330, y = 37)
        
        #Entry to input the username
        self.label_username = Label(self.frame, text = "Username")
        self.label_username.config(bg = RGB((84,146,203)))
        self.label_username.place(x = 10, y = 30)
        
        self.input_username = Entry(self.frame)
        self.input_username.place(x = 10, y = 50)
        
        #Combobox to show all the users connected
        self.label_show_users = Label(self.frame, text = "Connected Users:")
        self.label_show_users.config(bg = RGB((84,146,203)))
        self.label_show_users.place(x = 10, y = 90)
        
        self.show_all_the_users = ttk.Combobox(self.frame, state  = "readonly")
        self.show_all_the_users.set("Connected Users")
        self.show_all_the_users.config(width = 30, height = 20)
        self.show_all_the_users.place(x =30, y = 130)
        
        #button to chat with other user
        self.button_send = Button(self.frame, text = "chat", command =lambda: self.chat_to(self.show_all_the_users.get()," ", False))
        self.button_send.config(bg = RGB((84,146,203)), width = 8, height = 2)
        self.button_send.place(x = 300, y = 320)
        
        self.root.bind("<Return>",self.logic_button_connect_server)
        
        if self.root.mainloop() != True:
            self.server.send("exit".encode("utf-8"))
            self.kill_thread = True
            self.threading = None
            self.thread_get_message = None
            
            self.server = None
            sleep(0.5)
            print("Adios")
            
            
        self.root.mainloop()
    
    #method that is called when the button connect_server is pressed
    def logic_button_connect_server(self, event):
        username = self.input_username.get()
        if username == "":
            messagebox.showinfo("!","Debes ingresar un username")
        elif self.input_host_address.get() == "":
            messagebox.showinfo("!","Debes ingresar un host address")     
        else:          
            if self.server == None:
                self.server = socket.socket()
        
            host_address = list(self.input_host_address.get().split(":"))
            host = str(host_address[0])
            port = int(host_address[1])
            
            try:
                self.server.connect((host, port))
                self.server.send(username.encode("utf-8"))
                sleep(0.5)
                self.get_all_users_connected()
                self.thread_get_message = self.threading.Thread(target = self.get_new_user_connected)
                self.thread_get_message.start()
            except:
                messagebox.showinfo("!", "Error to connect to the server")
                self.server = None           
    
    #function that connect with other user to chat with him
    def chat_to(self, user_chat, first_message, opened_with):
        user = user_chat
        if user == "" or user == "Conected Users" or user == self.input_username.get() or user == f" {self.input_username.get()}":
            messagebox.showinfo("!","Debes ingresar un usuario valido")
        else:
            self.lock.acquire()    
            Windows_chat.Windows_chat(user, self.server, first_message, opened_with)
            

               
    #function that show all the connected users    
    def get_all_users_connected(self):
        try:
            self.server.send("give_me_all_users".encode("utf-8")) 
            users = str(self.server.recv(1024).decode("utf-8"))  
            if users != "":
                connected_users = list(users.split(","))
                self.input_host_address.config(state = "disabled")
                self.input_username.config(state = "disabled")
                self.button_connect_server.config(state = "disabled")
            for user in connected_users:
                user_cleaned = user.replace("[","")
                user_cleaned = user_cleaned.replace("]","")
                user_cleaned = user_cleaned.replace("'","")
                if user_cleaned not in self.show_all_the_users["values"] and f" {user_cleaned}" not in self.show_all_the_users["values"]:
                    self.list_of_users.append(user_cleaned)
                    self.show_all_the_users['values'] = self.list_of_users        
        except:
            messagebox.showinfo("Error", "Error al obtener los usuarios") 
    
    def get_new_user_connected(self):
        while True:
            message = self.server.recv(1024).decode("utf-8")
            if message == "exit":
                break
            if "private_chat:" in message:
                pass  
            if "new_user:" in message:
                message = list(message.split(":"))
                if self.list_of_users.count(message[1]) == 0 and f" {message[1]}" not in self.show_all_the_users["values"]:
                    self.list_of_users.append(message[1])
                    self.show_all_the_users['values'] = self.list_of_users       
            elif "message_from:" in message:
                message = list(message.split(":"))
                self.chat_to(message[1], message[2], True) 
                self.lock.acquire() 
            if self.kill_thread == True:
                break                     
                       
Lobin()   
 

    