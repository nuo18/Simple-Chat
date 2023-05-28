import tkinter as tk
import tkinter.font as font
import threading
import server, client
import re
import time

# Colours
BG_COLOR = "#F5F5F5"
SEND_COLOR = "#57aaa0"
RECEIVE_COLOR = "#E0E0E0"
TEXT_COLOR = "#212121"
ERROR_COLOR = "#D90202"

# Variables
END = "ML?NZ3d$s85E'AnfFM[Pdqk43@}~"

# Merge of classes

class SimpleChat:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x600")
        self.master.config(background=BG_COLOR)

        self.SERVER_RUNNING = False

        self.login_gui()


    def login_gui(self):
        # TODO: Should also include a way to timeout if the ip or port is incorrect
                
        self.master.title("Login")

        # Create widgets
        self.login_frame = tk.Frame(self.master, bg=BG_COLOR)
        self.login_frame.pack(pady=20)

        
        self.ip_label = tk.Label(self.login_frame, text="IP Address:", font=("Helvetica", 12), bg=BG_COLOR)
        self.ip_label.pack()
        
        self.ip_input = tk.Entry(self.login_frame, width=50, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR)
        self.ip_input.pack()
        self.ip_error = tk.Label(self.login_frame, width=50, font=("Helvetica", 10), fg=ERROR_COLOR, bg=BG_COLOR)
        self.ip_error.pack()

        self.port_label = tk.Label(self.login_frame, text="Port:", font=("Helvetica", 12), bg=BG_COLOR)
        self.port_label.pack()

        self.port_input = tk.Entry(self.login_frame, width=50, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR)
        self.port_input.insert(0, "8468")
        self.port_input.pack()
        self.port_error = tk.Label(self.login_frame, width=50, font=("Helvetica", 10), fg=ERROR_COLOR, bg=BG_COLOR)
        self.port_error.pack()

        self.username_label = tk.Label(self.login_frame, text="Username:", font=("Helvetica", 12), bg=BG_COLOR)
        self.username_label.pack()

        self.username_input = tk.Entry(self.login_frame, width=50, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR)
        self.username_input.pack()
        self.username_error = tk.Label(self.login_frame, width=50, font=("Helvetica", 10), fg=ERROR_COLOR, bg=BG_COLOR)
        self.username_error.pack()

        self.login_button = tk.Button(self.master, text="Login", command=self.login, bg=SEND_COLOR, fg="white", font=("Helvetica", 12), width=10, height=2)
        self.login_button.pack(pady=10)

        if self.SERVER_RUNNING:
            server_text = "Stop Server"
        else:
            server_text = "Start Server"

        self.start_button = tk.Button(self.master, text=server_text, command=self.start_server, bg=SEND_COLOR, fg="white", font=("Helvetica", 12), width=10, height=2)
        self.start_button.pack(pady=10)
        
        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.destroy, bg="red"
                                        , fg="white", font=("Helvetica", 12), width=10, height=2)
        self.exit_button.pack(pady=10)


        # Set font for all widgets
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=12)

    def login(self):
        ip_address = self.ip_input.get()
        port = self.port_input.get()
        username = self.username_input.get()
        valid = True

        # Reset the error messages (in case they previously existed)
        self.ip_error.config(text="")
        self.port_error.config(text="")
        self.username_error.config(text="")

        # TODO Check that all the fields are in the correct format

        try:
            port = int(port)
        except:
            self.port_error.config(text="Port must be an integer")
            valid = False


        if not username:
            self.username_error.config(text="You must have a username")
            valid = False

        if ip_address:
            ip_format = "^([0-9]|[1-9][0-9]|[1-9][0-9]{2})\.([0-9]|[1-9][0-9]|[1-9][0-9]{2})\.([0-9]|[1-9][0-9]|[1-9][0-9]{2})\.([0-9]|[1-9][0-9]|[1-9][0-9]{2})$"
            rex = re.compile(ip_format)
            if not rex.match(ip_address):
                self.ip_error.config(text="Ip address must be in the correct format")
                valid = False
        else:
            self.ip_error.config(text="You need an ip address")
            valid = False

        if valid:
            # Clear the current screen and put the chat gui
            self.clear()
            gui = self.chat_gui(ip_address, port, username)
    
    def start_server(self):
        # TODO Add an a way to verify whether the server is running or not and update the server accordingly

        if self.SERVER_RUNNING:
            print("Stop server")
            self.server.stopServer()
            self.SERVER_RUNNING = False
            self.start_button.config(text="Start Server")

        else:
            print("Start server")
            server_port = self.port_input.get()
            self.server = ""

            # Check whether a port is input
            # If a port is input, make sure it is an int
            # Otherwise use the default port
            if server_port:
                try:
                    server_port = int(server_port)
                    self.server = server.Server(port=server_port)

                except: 
                    self.port_error.config(text="Port must be an integer")
            else:
                server_port = 8468
                self.server = server.Server(port=server_port)
            
            # Start the server as a thread
            if self.server:
                self.server_thread = threading.Thread(target = self.server.startServer)
                self.server_thread.start()
                self.start_button.config(text="Stop Server")
                self.SERVER_RUNNING = True
            #Implement GUI to give server status


    def chat_gui(self, ip_address, port, username):

        self.master.title("Simple Chat")
                
        # Intializing the variables to be used
        self.ip = ip_address
        self.port = port
        self.username = username

        # Create client object and connect to server
        self.client = client.Client(self.ip, self.username, port=self.port)
        self.client.connect()
        
        self.run = True
        
        # Create widgets
        
        self.back_button = tk.Button(self.master, text="Back", command=self.leave_chat)
        self.back_button.pack()
        
        self.message_frame = tk.Frame(self.master, bg=BG_COLOR)
        self.message_frame.pack(pady=20)

        self.message_box = tk.Text(self.message_frame, width=50, height=20, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR, state="disabled", padx=10, pady=10)
        self.message_box.pack(side=tk.LEFT)

        self.send_button = tk.Button(self.master, text="Send", command=self.send_message, bg=SEND_COLOR, fg="white", font=("Helvetica", 12), width=10, height=2)
        self.send_button.pack(pady=10)

        self.input_box = tk.Entry(self.master, width=50, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR)
        self.input_box.pack(pady=10)

        # Set font for all widgets
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=12)

        self.recieve_thread = threading.Thread(target=self.recieve_messages)
        self.recieve_thread.start()

    def send_message(self):
        message = self.input_box.get()
        username = self.username
        
        # Append the message to the message box
        #self.message_box.configure(state='normal')
        #self.message_box.insert(tk.END, username + ": ", ("username", "blue"))
        #self.message_box.insert(tk.END, message + "\n")
        #self.message_box.configure(state='disabled')

        self.client.sendMessage(message)
        
        # Change the font and text color of the text in the message box
        self.message_box.tag_configure("username", font=("Helvetica", 12, "bold"), foreground="#007bff")
        self.input_box.delete(0, tk.END) # deletes the text in the entry box
        
    
    def recieve_messages(self):
        while self.run:
            message = self.client.recieve()
            if message == END:
                break
            self.message_box.configure(state='normal')
            self.message_box.insert(tk.END, str(message) + "\n", ("username", "blue"))
            self.message_box.configure(state='disabled')

    def leave_chat(self):
        # Close connection with server
        self.client.sendMessage(END)
        self.client.closeConnection()
        self.run = False
        # Ensure thread is ended before leaving
        self.recieve_thread.join()
        # Clear the window
        self.clear()
        # Load login screen
        self.login_gui()
    

    # Clears all the the contents of the master
    def clear(self):
        for i in self.master.grid_slaves():
            i.destroy()

        for i in self.master.pack_slaves():
            i.destroy()
    
    



# # TODO Need to merge both classes I think (in progress)
# class LoginGUI:
#     def __init__(self, master):
#         # TODO: Should also include a way to timeout if the ip or port is incorrect
                
#         self.master = master
#         self.master.geometry("500x600")
#         self.master.title("Login")
#         self.master.config(background=BG_COLOR)

#         # Create widgets
#         self.login_frame = tk.Frame(self.master, bg=BG_COLOR)
#         self.login_frame.pack(pady=20)

        
#         self.ip_label = tk.Label(self.login_frame, text="IP Address:", font=("Helvetica", 12), bg=BG_COLOR)
#         self.ip_label.pack()
        
#         self.ip_input = tk.Entry(self.login_frame, width=50, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR)
#         self.ip_input.pack()
#         self.ip_error = tk.Label(self.login_frame, width=50, font=("Helvetica", 10), fg=ERROR_COLOR, bg=BG_COLOR)
#         self.ip_error.pack()

#         self.port_label = tk.Label(self.login_frame, text="Port:", font=("Helvetica", 12), bg=BG_COLOR)
#         self.port_label.pack()

#         self.port_input = tk.Entry(self.login_frame, width=50, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR)
#         self.port_input.insert(0, "8468")
#         self.port_input.pack()
#         self.port_error = tk.Label(self.login_frame, width=50, font=("Helvetica", 10), fg=ERROR_COLOR, bg=BG_COLOR)
#         self.port_error.pack()

#         self.username_label = tk.Label(self.login_frame, text="Username:", font=("Helvetica", 12), bg=BG_COLOR)
#         self.username_label.pack()

#         self.username_input = tk.Entry(self.login_frame, width=50, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR)
#         self.username_input.pack()
#         self.username_error = tk.Label(self.login_frame, width=50, font=("Helvetica", 10), fg=ERROR_COLOR, bg=BG_COLOR)
#         self.username_error.pack()

#         self.login_button = tk.Button(self.master, text="Login", command=self.login, bg=SEND_COLOR, fg="white", font=("Helvetica", 12), width=10, height=2)
#         self.login_button.pack(pady=10)

#         self.start_button = tk.Button(self.master, text="Start Server", command=self.start_server, bg=SEND_COLOR, fg="white", font=("Helvetica", 12), width=10, height=2)
#         self.start_button.pack(pady=10)
        
#         self.exit_button = tk.Button(self.master, text="Exit", command=self.master.destroy, bg="red"
#                                         , fg="white", font=("Helvetica", 12), width=10, height=2)
#         self.exit_button.pack(pady=10)


#         # Set font for all widgets
#         default_font = font.nametofont("TkDefaultFont")
#         default_font.configure(size=12)


#     def login(self):
#         ip_address = self.ip_input.get()
#         port = self.port_input.get()
#         username = self.username_input.get()
#         valid = True

#         # Reset the error messages (in case they previously existed)
#         self.ip_error.config(text="")
#         self.port_error.config(text="")
#         self.username_error.config(text="")

#         # TODO Check that all the fields are in the correct format

#         try:
#             port = int(port)
#         except:
#             self.port_error.config(text="Port must be an integer")
#             valid = False


#         if not username:
#             self.username_error.config(text="You must have a username")
#             valid = False

#         if ip_address:
#             ip_format = "^([0-9]|[1-9][0-9]|[1-9][0-9]{2})\.([0-9]|[1-9][0-9]|[1-9][0-9]{2})\.([0-9]|[1-9][0-9]|[1-9][0-9]{2})\.([0-9]|[1-9][0-9]|[1-9][0-9]{2})$"
#             rex = re.compile(ip_format)
#             if not rex.match(ip_address):
#                 self.ip_error.config(text="Ip address must be in the correct format")
#                 valid = False
#         else:
#             self.ip_error.config(text="You need an ip address")
#             valid = False

#         if valid:

#             # Clear the current screen and put the chat gui
#             self.clear()
#             gui = ChatGUI(root, ip_address, port, username)
    
#     def start_server(self):
#         # TODO Add an a way to verify whether the server is running or not and update the server accordingly

#         server_port = self.port_input.get()
#         self.server = ""

#         # Check whether a port is input
#         # If a port is input, make sure it is an int
#         # Otherwise use the default port
#         if server_port:
#             try:
#                 server_port = int(server_port)
#                 self.server = server.Server(port=server_port)

#             except: 
#                 self.port_error.config(text="Port must be an integer")
#         else:
#             server_port = 8468
#             self.server = server.Server(port=server_port)
        
#         # Start the server as a thread
#         if self.server:
#             self.server_thread = threading.Thread(target = self.server.startServer)
#             self.server_thread.start()
#             self.start_button.config(text="Stop Server")
#             SERVER_RUNNING = True
#         #Implement GUI to give server status



#     # Clears all the the contents of the master
#     def clear(self):
#         for i in self.master.grid_slaves():
#             i.destroy()

#         for i in self.master.pack_slaves():
#             i.destroy()

# class ChatGUI:
#     def __init__(self, master, ip_address, port, username):
#         self.master = master
#         self.master.geometry("500x600")
#         self.master.title("Simple Chat")
#         self.master.config(background=BG_COLOR)
        
#         # Intializing the variables to be used
#         self.username = username
#         self.ip = ip_address
#         self.port = port

#         # Create client object and connect to server
#         self.client = client.Client(self.ip, self.username, port=self.port)
#         self.client.connect()
        
#         self.run = True
        
#         # Create widgets
        
#         self.back_button = tk.Button(self.master, text="Back", command=self.leave_chat)
#         self.back_button.pack()
        
#         self.message_frame = tk.Frame(self.master, bg=BG_COLOR)
#         self.message_frame.pack(pady=20)

#         self.message_box = tk.Text(self.message_frame, width=50, height=20, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR, state="disabled", padx=10, pady=10)
#         self.message_box.pack(side=tk.LEFT)

#         self.send_button = tk.Button(self.master, text="Send", command=self.send_message, bg=SEND_COLOR, fg="white", font=("Helvetica", 12), width=10, height=2)
#         self.send_button.pack(pady=10)

#         self.input_box = tk.Entry(self.master, width=50, font=("Helvetica", 12), fg=TEXT_COLOR, bg=RECEIVE_COLOR)
#         self.input_box.pack(pady=10)

#         # Set font for all widgets
#         default_font = font.nametofont("TkDefaultFont")
#         default_font.configure(size=12)

#         self.recieve_thread = threading.Thread(target=self.recieve_messages)
#         self.recieve_thread.start()

#     def send_message(self):
#         message = self.input_box.get()
#         username = self.username
        
#         # Append the message to the message box
#         #self.message_box.configure(state='normal')
#         #self.message_box.insert(tk.END, username + ": ", ("username", "blue"))
#         #self.message_box.insert(tk.END, message + "\n")
#         #self.message_box.configure(state='disabled')

#         self.client.sendMessage(message)
        
#         # Change the font and text color of the text in the message box
#         self.message_box.tag_configure("username", font=("Helvetica", 12, "bold"), foreground="#007bff")
#         self.input_box.delete(0, tk.END) # deletes the text in the entry box
        
    
#     def recieve_messages(self):
#         while self.run:
#             message = self.client.recieve()
#             if message == END:
#                 break
#             self.message_box.configure(state='normal')
#             self.message_box.insert(tk.END, str(message) + "\n", ("username", "blue"))
#             self.message_box.configure(state='disabled')

#     def leave_chat(self):
#         # Close connection with server
#         self.client.sendMessage(END)
#         self.client.closeConnection()
#         self.run = False
#         # Ensure thread is ended before leaving
#         self.recieve_thread.join()
#         # Clear the window
#         self.clear()
#         # Load login screen
#         LoginGUI(self.master)

#     # Clears all the the contents of the master
#     def clear(self):
#         for i in self.master.grid_slaves():
#             i.destroy()

#         for i in self.master.pack_slaves():
#             i.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    simple_chat = SimpleChat(root)
    # The login method of the LoginGUI class will destroy the login window
    # and create an instance of the ChatGUI class with the login details

    root.mainloop()
