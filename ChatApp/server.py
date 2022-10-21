import socket
import threading

class Server():
    def __init__(self, server,username, client, usernames, clients):
        
        self.server = server
        self.usernames = usernames
        self.clients = clients
        
        
        #datos del cliente
        self.username = username
        self.client = client 
        self.message = ""
        self.list_message = []
        self.chat_to = ""   
    
    def handle_clients(self):
        print(f"{self.username} have been connected")
        self.tell_all_new_user_connected()
        while True:
            try:
                self.message = self.client.recv(1024).decode('utf-8')
                print(f"{self.username}:{self.message}")
            
                if self.message == "exit":
                    print(f"{self.username} have been disconnected")
                    self.client.send(f"exit".encode("utf-8"))
                    self.clients.remove(self.clients[self.usernames.index(self.username)])
                    self.usernames.remove(self.username)
                    break
                
                if "chat_to:" in self.message:
                    self.list_message = list(self.message.split(":"))
                    self.chat_to = self.clients[self.usernames.index(self.list_message[1])] 
                    self.chat_with()
                if "private_chat:" in self.message:
                    self.list_message = list(self.message.split(":"))
                    self.chat_to = self.clients[self.usernames.index(self.list_message[1])] 
                    self.private_chat()    
                if self.message == "give_me_all_users":
                    self.client.send(f"{self.usernames}".encode("utf-8"))
                
            except:
                print("Ha ocurrido un error")
                break    
                
    def chat_with(self):
         self.chat_to.send(f"message_from:{self.username}:{self.list_message[2]}".encode("utf-8")) 
    def private_chat(self):
        self.chat_to.send(f"private_chat:{self.username}:{self.list_message[2]}".encode("utf-8"))
    def tell_all_new_user_connected(self):
        for client in self.clients:
            if client == self.client:
                pass
            else:
                client.send(f"new_user:{self.username}".encode("utf-8"))                  

host = "localhost"
port = 8888

#start the server
server = socket.socket()
server.bind((host,port))
server.listen()
print(f"server running on {host}:{port}")

#list that contains users and usernames
clients = []
usernames = []

def recive_clients():
    while True:
        client, address = server.accept()
        username = client.recv(1021).decode('utf-8')
        if username in usernames:
            username += "1"
        clients.append(client)
        usernames.append(username)
        threading.Thread(target=Server(server, username, client, usernames, clients).handle_clients).start() 

recive_clients()                       