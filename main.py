import tkinter
import customtkinter  # <- import the CustomTkinter module

class DisplayMain():
    def __init__(self):
        self.root_tk = tkinter.Tk()  # create the Tk window like you normally do
        self.root_tk.geometry("400x240")
        self.root_tk.title("CustomTkinter Test")

        # Colours
        Black = "#253649"
        Teal = "57aaa0"

        self.root_tk.config(background=Black, width=500, height=600)

        
        # Use CTkButton instead of tkinter Button
        self.button = customtkinter.CTkButton(master=self.root_tk, corner_radius=10, command=button_function)
        self.button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        #insert commands for layout


        self.root_tk.mainloop()

    def button_function(self):
        print("button pressed")

    
    
