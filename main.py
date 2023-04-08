import tkinter as tk
import tkinter.font as font
import server, client

# Colours
BG_COLOR = "#F5F5F5"
SEND_COLOR = "#57aaa0"
RECEIVE_COLOR = "#E0E0E0"
TEXT_COLOR = "#212121"

class ChatGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x600")
        self.master.title("Simple Chat")
        self.master.config(background=BG_COLOR)

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

    def send_message(self):
        message = self.input_box.get()
        # Implement logic for sending message to server/client

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatGUI(root)
    root.mainloop()
