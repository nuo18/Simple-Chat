import tkinter
import customtkinter as cs  # <- import the CustomTkinter module
import server, client

# Colours
Black = "#282424"
Teal = "57aaa0"

root = tkinter.Tk()  # create the Tk window like you normally do
root.geometry("500x600")
root.title("Simple Chat")
root.config(background=Black)

root.mainloop()