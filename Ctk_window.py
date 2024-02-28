import tkinter
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("./custom_theme.json")


app = customtkinter.CTk()
app.configure(bg='systemTransparent')
app.geometry("1024x768")
app.attributes('-alpha', 0.5)

title = customtkinter.CTkLabel(app, text="testing")
title.pack(padx=10, pady=10)

app.mainloop()