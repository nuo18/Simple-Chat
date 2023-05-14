import socket 
import threading

class Client():
    def __init__(self, host, username, port=8468):
        self.host = host
        self.port = port
        self.nickname = username

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setNickname(self, nickname):
        self.nickname = nickname
    
    def connect(self):
        self.client.connect((self.host, self.port))
        self.client.send(self.nickname.encode("ascii"))

    def sendMessage(self, message):
        message = f"{self.nickname}: {message}"
        self.client.send(message.encode('ascii'))

    def recieve(self):
        try:
            message = self.client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                self.client.send(self.nickname.encode('ascii'))
            else:
                return message
        except:                                                 #case on wrong ip/port details
            return int(987)
            self.client.close()
