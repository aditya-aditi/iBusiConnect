import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def startingWinFunc():
    startingWindow = ctk.CTk()
    startingWindow.geometry("896x510")

    startingLabel = ctk.CTkLabel(master=startingWindow, text="Welcome to iBusiConnect", font=("Lucida Handwriting", 60), text_color="#ffffff")
    startingLabel.pack(pady=220) 

    startingWindow.after(1500,lambda:startingWindow.destroy())

    startingWindow.mainloop()

if __name__ == "__main__":
    startingWinFunc()