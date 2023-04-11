import tkinter as tk
import tkinter.font as font
import threading
import socketserver

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = str(self.request.recv(1024), 'utf-8')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'utf-8')
        self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        self.server_thread = None

    def start(self):
        self.server = ThreadedTCPServer((self.host, self.port), ThreadedTCPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.server_thread.join()


# Colours
BG_COLOR = "#F5F5F5"
SEND_COLOR = "#57aaa0"
RECEIVE_COLOR = "#E0E0E0"
TEXT_COLOR = "#212121"

import socket
import threading

class Client:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))
        self.socket.sendall(self.username.encode())

    def send_message(self, message):
        self.socket.sendall(message.encode())

    def receive_messages(self, chat_gui):
        while True:
            message = self.socket.recv(1024).decode()
            chat_gui.append_message(message)

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}...")

        while True:
            client_socket, client_address = self.socket.accept()
            client_username = client_socket.recv(1024).decode()
            print(f"New connection from {client_address[0]}:{client_address[1]} as {client_username}")
            self.clients[client_socket] = client_username
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            message = client_socket.recv(1024).decode()
            if message:
                username = self.clients[client_socket]
                print(f"{username}: {message}")
                for socket in self.clients:
                    if socket != client_socket:
                        socket.sendall(f"{username}: {message}".encode())
            else:
                username = self.clients[client_socket]
                print(f"Connection from {username} closed.")
                del self.clients[client_socket]
                client_socket.close()
                break


class LoginGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x600")
        self.master.title("Login")
        self.master.config(background=BG_COLOR)

        # Create widgets
        self.login_frame = tk.Frame(self.master, bg=BG_COLOR)
        self.login_frame.pack(pady=20)

        self.ip_label = tk.Label(self.login_frame, text="IP Address:", font=("Helvetica", 12), bg=BG_COLOR)
        self.ip_label.pack()

        self.ip_input = tk.Entry(self.login_frame, width=50, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR)
        self.ip_input.pack()

        self.port_label = tk.Label(self.login_frame, text="Port:", font=("Helvetica", 12), bg=BG_COLOR)
        self.port_label.pack()

        self.port_input = tk.Entry(self.login_frame, width=50, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR)
        self.port_input.pack()

        self.username_label = tk.Label(self.login_frame, text="Username:", font=("Helvetica", 12), bg=BG_COLOR)
        self.username_label.pack()

        self.username_input = tk.Entry(self.login_frame, width=50, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR)
        self.username_input.pack()

        self.login_button = tk.Button(self.master, text="Login", command=self.login, bg=SEND_COLOR, fg="white", font=("Helvetica", 12), width=10, height=2)
        self.login_button.pack(pady=10)
        
        self.start_button = tk.Button(self.master, text="Start Server", command=self.start_server, bg=SEND_COLOR, fg="white", font=("Helvetica", 12), width=10, height=2)
        self.start_button.pack(pady=10)
        
        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.destroy, bg="red"
                                        , fg="white", font=("Helvetica", 12), width=10, height=2)
        self.exit_button.pack(pady=10)


        # Set font for all widgets
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=12)

    def login(self):
        ip_address = self.ip_input.get()
        port = int(self.port_input.get())
        username = self.username_input.get()

        # Hide login window and show chat window
        self.master.destroy()
        
        client = Client(ip_address, port, username)
        client.connect()

        root = tk.Tk()
        gui = ChatGUI(root, client, username)
        receive_thread = threading.Thread(target=client.receive_messages, args=(gui,))
        receive_thread.start()
        
        root.mainloop()

        # Implement logic for sending login details to server/client
    
    def start_server(self):
        self.chat_server = ChatServer(self.host, self.port)
        self.chat_server.start()


class ChatGUI:
    def __init__(self, master, ip_address, port, username):
        self.master = master
        self.master.geometry("500x600")
        self.master.title("Simple Chat")
        self.master.config(background=BG_COLOR)
        
        # Intializing the variables to be used
        self.username = username
        self.ip = ip_address
        self.port = port

        # Create widgets
        self.message_frame = tk.Frame(self.master, bg=BG_COLOR)
        self.message_frame.pack(pady=20)

        self.message_box = tk.Text(self.message_frame, width=50, height=20, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR, padx=10, pady=10)
        self.message_box.pack(side=tk.LEFT)

        self.send_button = tk.Button(self.master, text="Send", command=self.send_message, bg=SEND_COLOR, fg="white", font=("Helvetica", 12), width=10, height=2)
        self.send_button.pack(pady=10)

        self.input_box = tk.Entry(self.master, width=50, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR)
        self.input_box.pack(pady=10)

        # Set font for all widgets
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=12)
        
        # Create a socket object
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        self.sock.connect((self.ip, self.port))

        # Send the username to the server
        self.sock.send(username.encode())

        # Start a separate thread to receive messages from the server
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def send_message(self):
        message = self.input_box.get()
        username = self.username
        
        # Send the message to the server
        self.sock.send(message.encode())
        
        # Append the message to the message box
        self.message_box.configure(state='normal')
        self.message_box.insert(tk.END, username + ": ", ("username", "blue"))
        self.message_box.insert(tk.END, message + "\n")
        self.message_box.configure(state='disabled')
        
        # Change the font and text color of the text in the message box
        self.message_box.tag_configure("username", font=("Helvetica", 12, "bold"), foreground="#007bff")
        self.input_box.delete(0, tk.END) # deletes the text in the entry box
        # Implement logic for sending message to server/client
    
    def receive_messages(self):
        while True:
            try:
                # Receive messages from the server
                message = self.sock.recv(1024).decode()

                # Append the message to the message box
                self.message_box.configure(state='normal')
                self.message_box.insert(tk.END, message)
                self.message_box.configure(state='disabled')
            except:
                # If an error occurs, close the socket and exit the loop
                self.sock.close()
                break



if __name__ == "__main__":
    root = tk.Tk()
    login_gui = LoginGUI(root)

    # The login method of the LoginGUI class will destroy the login window
    # and create an instance of the ChatGUI class with the login details
    root.mainloop()
