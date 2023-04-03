import socket 
import threading

class Client():
    def __init__(self, host, port=8468):
        self.host = host
        self.port = port
        self.nickname

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setNickname(self, nickname):
        self.nickname = nickname
    
    def connect(self):
        self.client.connect((self.host, self.port))

    def sendMessage(self, message):
        self.client.send(f"{self.nickname}: {message}")

    def recieve(self):
        while True:                                                 #making valid connection
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICKNAME':
                    self.client.send(self.nickname.encode('ascii'))
                else:
                    print(message)
                    return message
            except:                                                 #case on wrong ip/port details
                print("An error occured!")
                self.client.close()
                break
