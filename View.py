import tkinter
import customtkinter
from PIL import Image

class View:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.create_app()

    def create_app(self):
        #set sys. settings
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")
        #initiate app frame
        self.app.geometry("300x300")
        self.app.title("Tamagotchi")
        my_image = customtkinter.CTkImage(light_image=Image.open("Assets/Images/light_castle.png"),
                                          dark_image=Image.open("Assets/Images/dark_castle.png"),
                                          size=(300,300))
        #Image label
        image_label = customtkinter.CTkLabel(self.app, image=my_image, text="")
        image_label.pack(padx=0, pady=0)

        #Run the app
        self.app.mainloop()