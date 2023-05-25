import socket
import threading

END = "ML?NZ3d$s85E'AnfFM[Pdqk43@}~"

class Server():
    def __init__(self, host=socket.gethostbyname(socket.gethostname()), port=8468):
        self.host = host
        self.port = port

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
                #print("A message has been recieved")
                if len(message) == 0 or message.decode() == END:
                    raise Exception("Connection closed")
                else:
                    self.sendMessage(message)
            except:
                nickname = self.clients[client]

                client.close()
                self.clients.pop(client)
                self.sendMessage(f'{nickname} left!'.encode('ascii'))
                #print("SERVER LEAVING MESSAGE")
                print(f'{nickname} left!')
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

    def stopServer(self):
        for client in self.clients:
            client.close()

        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        
