import socket 
import threading

END = "ML?NZ3d$s85E'AnfFM[Pdqk43@}~"

class Client():
    def __init__(self, host, username, port=8468):
        self.host = host
        self.port = port
        self.nickname = username

        self.nickname_sent = False

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setNickname(self, nickname):
        self.nickname = nickname
    
    def connect(self):
        self.client.connect((self.host, self.port))
        #self.client.send(self.nickname.encode("ascii"))

    def sendMessage(self, message):
        if message != END:
            message = f"{self.nickname}: {message}"
        self.client.send(message.encode('ascii'))

    def recieve(self):
        try:
            message = self.client.recv(1024).decode('ascii')
            if len(message) == 0 or message == END:
                raise Exception("Connection Closed")
            
            if message == 'NICKNAME' and not self.nickname_sent:
                self.client.send(self.nickname.encode('ascii'))
                self.nickname_sent = True
            else:
                return message

        except:                                                 #case on wrong ip/port details
            self.client.close()
            return END
            
    def closeConnection(self):
        self.client.close()
