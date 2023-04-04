import tkinter
import customtkinter as cs  # <- import the CustomTkinter module
import server, client

# CTK: https://github.com/TomSchimansky/CustomTkinter/wiki/

# Colours
Black = "#282424"
Teal = "57aaa0"

root = tkinter.Tk()  # create the Tk window like you normally do
root.geometry("500x600")
root.title("Simple Chat")
root.config(background=Black)


#? Text Box Entry
entry = cs.CTkEntry(root, width=400, height=40, font=('Helvetica 12'))
entry.place(relx=0.45, rely=0.95, anchor=tkinter.CENTER) # relx/rely is relative position, IDK what anchor is
# We can use relative x ( horizontal ) and y ( vertical ) position with respect to width and 
# height of the window by using relx and rely options. relx=0 is left edge of the window relx=1 
# is right edge of the window. rely=0 is top of the window and rely=1 is the bottom edge of the window.

#? Button to send
send_button = cs.CTkButton(root, width=20, height=20)
#! Fix error
send_button.place(relx=0.55, rely=0.95, anchor=tkinter.CENTER)

root.mainloop()