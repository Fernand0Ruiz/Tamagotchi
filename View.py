import tkinter
import customtkinter as ctk
from PIL import Image
from Controller import Controller
from Model import Model
from Sprite_Animator import SpriteAnimator

#Mood Image paths to be set based off stats.
mood_imgs = [
    "Assets/Moods/mood_angry.png",
    "Assets/Moods/mood_dance.png",
    "Assets/Moods/mood_happy.png",
    "Assets/Moods/mood_middle.png",
    "Assets/Moods/mood_sad.png",
    "Assets/Moods/mood_sleep.png"
]

#Main assest, backgrounds, logos, etc. 
bg_imgs = [
    "Assets/logo.png",
    "Assets/light_background.png",
    "Assets/dark_background.png",
    "Assets/save_icon.png"
]

#Main interaction buttons images.
button_imgs = [
    "Assets/Buttons/dice.png",
    "Assets/Buttons/oniguri.png",
    "Assets/Buttons/dance.png",
    "Assets/Buttons/lanturn.png"
]

#Main font.
font = ("Andale Mono", 12)

class View:
    def __init__(self):
        self.app = ctk.CTk()
        self.tamagotchi = Model()
        self.controller = Controller(self.tamagotchi)
        self.create_app()
        #self.sprite_animator = SpriteAnimator(self.app)

    def run(self):
        self.app.mainloop()

    def create_app(self):
        #set sys. settings, app settings, and background img.
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.app.geometry("300x400")
        self.app.title("Tamagotchi")
        self.app.resizable(False, False)  #Lock both width and height
        my_image = ctk.CTkImage(light_image=Image.open(bg_imgs[1]),
                                dark_image=Image.open(bg_imgs[1]),
                                size=(300,400))
        image_label = ctk.CTkLabel(self.app, image=my_image, text="")
        image_label.pack(padx=0, pady=0)

        self.make_labels("Sekitoritchi", 0.43, 0.08, ("Andale Mono", 14), "#796344", "#E8D4AC", 100, 14)  
        self.make_labels("Age: ", 0.695, 0.08, font, "#796344", "#E8D4AC", 25, 14)
        self.make_labels("Wgt: ", 0.695, 0.124, font, "#796344", "#E8D4AC", 25, 14)
        self.make_labels("Mood", 0.85, 0.07, font, "#796344", "#E8D4AC", 25, 14)

        mood_image = ctk.CTkImage(Image.open(mood_imgs[2]),size=(25,25))
        mood_image_label = ctk.CTkLabel(self.app, image=mood_image, text="", bg_color="#E8D4AC",)
        mood_image_label.place(relx=0.85, rely=0.120, anchor="center")

        health_bar = ctk.CTkProgressBar(self.app, width=100, height=10, corner_radius=0,
                                        fg_color="#796344", progress_color="dark green")
        health_bar.pack(padx=0, pady=0)
        health_bar.set(0.75)
        health_bar.place(relx=0.435, rely=0.125, anchor="center")

        #create buttons
        self.make_buttons(self.show_menu, 0.17, 0.1025, bg_imgs[0], "#796344", 1, 35)
        for i in range(4):
            relx = 0.17 + (i * 0.22)
            self.make_buttons(self.controller.feed, relx, 0.906, button_imgs[i], "#D8C0A8", 2, 35)

        #self.sprite_animator.place(relx=0.5, rely=0.5, anchor="center")
        #self.sprite_animator.set_action("idle")


    def make_buttons(self, cmd, relx, rely, image_path=None, hover=None, border=None, size=None):
        button_image = ctk.CTkImage(Image.open(image_path), size=(size, size))
        button = ctk.CTkButton(self.app,text="", width=size, height=size,corner_radius=0,
                                fg_color="#EED9C4", hover_color=hover,border_width=border,
                                border_color="#796344",command=cmd,image=button_image)
        button.place(relx=relx, rely=rely, anchor="center")

    def make_labels(self, text, relx, rely, font, text_color, bg_color, width, height):
        label = ctk.CTkLabel(self.app, text=text, font=font, text_color=text_color, bg_color=bg_color,
                             width=width, height=height)
        label.place(relx=relx, rely=rely, anchor="center")

    def update_display(self):
        # Update your labels with current model data
        self.name_label.configure(text=self.model.name)
        self.age_label.configure(text=f"Age: {self.model.age}")
        self.weight_label.configure(text=f"Wgt: {self.model.weight}")
        # Update mood image
        mood_image = ctk.CTkImage(
            Image.open(mood_imgs[self.model.mood]),
            size=(25,25)
        )
        self.mood_image_label.configure(image=mood_image)
        # Update health bar
        self.health_bar.set(self.model.health)

    def show_menu(self):
        menu_window = ctk.CTkToplevel(self.app)
        menu_window.title("Menu")
        menu_window.geometry("200x200")
        menu_window.resizable(False, False)
        
        # Make the menu window stay on top
        menu_window.transient(self.app)
        menu_window.grab_set()

        # Create buttons
        buttons = [
            ("Save Game", self.controller.save_game),
            ("Load Game", self.controller.load_game),
            ("Exit", self.app.quit)
        ]

        # Create each button
        for text, command in buttons:
            button = ctk.CTkButton(
                menu_window,
                text=text,
                font=font,
                text_color="#796344",
                width=150,
                height=35,
                corner_radius=0,
                fg_color="#EED9C4",
                hover_color="#D8C0A8",
                border_width=2,
                border_color="#796344",
                command=command
            )
            button.pack(pady=5)

        