import tkinter as tk
import tkinter.font as font
import threading
import server, client
import re

# Colours
BG_COLOR = "#F5F5F5"
SEND_COLOR = "#57aaa0"
RECEIVE_COLOR = "#E0E0E0"
TEXT_COLOR = "#212121"
ERROR_COLOR = "#D90202"


class LoginGUI:
    def __init__(self, master):
        # TODO: Should also include a way to timeout if the ip or port is incorrect
        
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
        self.ip_error = tk.Label(self.login_frame, width=50, font=("Helvetica", 10), fg=ERROR_COLOR, bg=BG_COLOR)
        self.ip_error.pack()
        # TODO: Should include a way to check that the format of the ip is correct


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

            # Hide login window and show chat window
            self.master.destroy()

            root = tk.Tk()
            gui = ChatGUI(root, ip_address, port, username)
            root.mainloop()

            # Implement logic for sending login details to server/client
    
    def start_server(self):
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
            self.start_button.config(text="Started")
        #Implement GUI to give server status

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
        print(self.port)

        # Create client object and connect to server
        self.client = client.Client(self.ip, self.username, port=self.port)
        self.client.connect()
        
        

        # Create widgets
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
        while True:
            message = self.client.recieve()
            if "i" == int(987):
                break

            self.message_box.configure(state='normal')
            self.message_box.insert(tk.END, str(message) + "\n", ("username", "blue"))
            self.message_box.configure(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    login_gui = LoginGUI(root)

    # The login method of the LoginGUI class will destroy the login window
    # and create an instance of the ChatGUI class with the login details

    root.mainloop()
