import socket
import threading

class Server():
    def __init__(self, host=socket.gethostbyname(socket.gethostname()), port=8468):
        self.host = host
        self.port = port

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Dictionary containing clients and their nicknames
        self.clients = {} 

    def startServer(self):
        self.server.bind((self.host, self.port))
        self.server.listen()

        self.recieve()

    def sendMessage(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.sendMessage(message)
            except:
                nickname = self.clients[client]

                client.close()
                self.clients.pop(client)
                self.sendMessage(f'{nickname} left!')
                break
    
    def recieve(self):
        while True:
            client, address = self.server.accept()
            print(f"Connected with {address}")
            client.send("NICKNAME".encode("ascii"))
            nickname = client.recv(1024).decode('ascii')
            self.clients[client] = nickname
            print(f"Nickname is {nickname}")
            self.sendMessage(f"{nickname} joined!".encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()
