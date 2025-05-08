import tkinter
import customtkinter as ctk
from PIL import Image
from Controller import Controller

mood_imgs = [
    "/Users/fernandoruiz/Tamagotchi/Assets/Moods/mood_angry.png",
    "/Users/fernandoruiz/Tamagotchi/Assets/Moods/mood_dance.png",
    "/Users/fernandoruiz/Tamagotchi/Assets/Moods/mood_happy.png",
    "/Users/fernandoruiz/Tamagotchi/Assets/Moods/mood_middle.png",
    "/Users/fernandoruiz/Tamagotchi/Assets/Moods/mood_sad.png",
    "/Users/fernandoruiz/Tamagotchi/Assets/Moods/mood_sleep.png"
]

bg_imgs = [
    "/Users/fernandoruiz/Tamagotchi/Assets/logo.png",
    "/Users/fernandoruiz/Tamagotchi/Assets/light_background.png",
    "/Users/fernandoruiz/Tamagotchi/Assets/dark_background.png"
]

button_imgs = [
    "/Users/fernandoruiz/Tamagotchi/Assets/dice.png",
    "/Users/fernandoruiz/Tamagotchi/Assets/oniguri.png",
    "/Users/fernandoruiz/Tamagotchi/Assets/dance.png",
    "/Users/fernandoruiz/Tamagotchi/Assets/lanturn.png"
]

class View:
    def __init__(self):
        self.app = ctk.CTk()
        self.controller = Controller()
        self.create_app()

    def create_app(self):
        #set sys. settings
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        #initiate app frame
        self.app.geometry("300x400")
        self.app.title("Tamagotchi")
        self.app.resizable(False, False)  # Lock both width and height
        my_image = ctk.CTkImage(light_image=Image.open(bg_imgs[1]),
                                dark_image=Image.open(bg_imgs[1]),
                                size=(300,400))
        #Image label
        image_label = ctk.CTkLabel(self.app, image=my_image, text="")
        image_label.pack(padx=0, pady=0)

        name_label = ctk.CTkLabel(self.app, 
                             text="Sekitoritchi", 
                             font=("Andale Mono", 14),
                             text_color="#796344",
                             bg_color="#E8D4AC",
                             width=100,
                             height=14
                             )
        name_label.pack(padx=0, pady=0)
        name_label.place(relx=0.43, rely=0.08, anchor="center")

        age_label = ctk.CTkLabel(self.app, 
                             text="Age: ", 
                             font=("Andale Mono", 12),
                             text_color="#796344",
                             bg_color="#E8D4AC",
                             width=25,
                             height=14
                             )
        age_label.pack(padx=0, pady=0)
        age_label.place(relx=0.695, rely=0.08, anchor="center")

        weight_label = ctk.CTkLabel(self.app, 
                             text="Wgt: ", 
                             font=("Andale Mono", 12),
                             text_color="#796344",
                             bg_color="#E8D4AC",
                             width=25,
                             height=14
                             )
        weight_label.pack(padx=0, pady=0)
        weight_label.place(relx=0.685, rely=0.124, anchor="center")

        mood_label = ctk.CTkLabel(self.app,
            text="Mood",
            font=("Andale Mono", 12),
            text_color="#796344",
            bg_color="#E8D4AC",
            width=25,
            height=14
        )
        mood_label.pack(padx=0, pady=0)
        mood_label.place(relx=0.85,rely=0.07, anchor="center")


        mood_image = ctk.CTkImage(
            Image.open(mood_imgs[2]),
            size=(25,25)
        )
        mood_image_label = ctk.CTkLabel(self.app, image=mood_image, text="", bg_color="#E8D4AC",)
        mood_image_label.place(relx=0.85, rely=0.120, anchor="center")

        health_bar = ctk.CTkProgressBar(self.app, 
                                        width=100, 
                                        height=10,
                                        corner_radius=0,
                                        fg_color="#796344",
                                        progress_color="dark green"
                                        )
        health_bar.pack(padx=0, pady=0)
        health_bar.set(0.75)
        health_bar.place(relx=0.435, rely=0.125, anchor="center")

        logo = ctk.CTkImage(
            Image.open(bg_imgs[0]),
            size=(35, 35),  # Adjust size as needed
        )
        
        logo_button = ctk.CTkButton(
            self.app,
            text="",
            width=35,
            height=35,
            corner_radius=0,
            fg_color="#EED9C4",
            hover_color="#796344",
            border_width=1,
            border_color="#796344",
            command="",
            image=logo
        )
        logo_button.place(relx=0.17, rely=0.1025, anchor="center")


        #create buttons
        for i in range(4):
            relx = 0.17 + (i * 0.22)
            self.make_buttons(self.controller.feed, relx, 0.906, button_imgs[i])

    def run(self):
        self.app.mainloop()

    def make_buttons(self, cmd, relx, rely, image_path=None):
        # Create button image if path is provided
        button_image = None
        if image_path:
            button_image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(35, 35),  # Adjust size as needed
            )
        
        button = ctk.CTkButton(
            self.app,
            text="",
            width=0,
            height=0,
            corner_radius=0,
            fg_color="#EED9C4",
            hover_color="#D8C0A8",
            border_width=2,
            border_color="#796344",
            command=cmd,
            image=button_image
        )
        button.place(relx=relx, rely=rely, anchor="center")