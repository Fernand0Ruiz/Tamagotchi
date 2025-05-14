import tkinter
import customtkinter as ctk
from PIL import Image
from Controller import Controller
from Model import Model
from Animate import SpriteAnimator

#Mood Image paths to be set based off stats.
mood_imgs = [
    "Assets/Moods/mood_happy.png",
    "Assets/Moods/mood_middle.png",
    "Assets/Moods/mood_angry.png",
    "Assets/Moods/mood_sad.png",
    "Assets/Moods/mood_dance.png",
    "Assets/Moods/mood_sleep.png"
]

#Main assest, backgrounds, logos, etc. 
bg_imgs = [
    "Assets/logo.png",
    "Assets/layout.png",
    "Assets/dark_background.png",
    "Assets/save_icon.png"
]

#Main interaction buttons images.
button_imgs = [
    "Assets/Buttons/dice.png",
    "Assets/Buttons/lanturn.png",
    "Assets/Buttons/dance.png",
    "Assets/Buttons/oniguri.png"
]

font = ("Andale Mono", 10)
text_color = "black"
background_label_color = "#D5AF75"
button_color = "#EED9C4"
button_hover_color = "#D8C0A8"
button_border_color = "#796344"

class View:
    def __init__(self):
        self.app = ctk.CTk()
        self.tamagotchi = Model(self.app)
        self.controller = Controller(self.tamagotchi, self.app)
        self.tamagotchi.add_observer(self.update_view)
        self.name = None
        self.age = None
        self.weight = None
        self.mood_image = None
        self.health_bar = None
        self.sprite_animator = None
        self.create_app()

    def run(self):
        try:
            self.app.mainloop()
        finally:
            # Cleanup when window is closed
            if hasattr(self, 'tamagotchi'):
                self.tamagotchi.stop()

    def create_app(self):
        #set sys. settings, app settings, and background img.
        self.app.geometry("300x400")
        self.app.title("Tamagotchi")
        self.app.resizable(False, False)  #Lock both width and height
        my_image = ctk.CTkImage(Image.open(bg_imgs[1]), size=(300,400))
        image_label = ctk.CTkLabel(self.app, image=my_image, text="")
        image_label.pack(padx=0, pady=0)

        # Get pet stats from the controller
        pet_stats = self.controller.get_pet()

        #make sprite animator
        self.sprite_animator = SpriteAnimator(self.app, action=pet_stats["action"], background=pet_stats["background"])
        self.sprite_animator.place(relx=0.5, rely=0.505, anchor="center")

        #make labels
        self.name = self.make_labels(pet_stats["name"], 0.43, 0.08, ("Andale Mono", 14), text_color, background_label_color, 100, 14)  
        self.age = self.make_labels(f"Yrs:{pet_stats['age']}", 0.6725, 0.08, font, text_color, background_label_color, 25, 14)
        self.weight = self.make_labels(f"Lbs:{pet_stats['weight']}", 0.695, 0.124, font, text_color, background_label_color, 25, 14)
        mood = self.make_labels("Mood", 0.85, 0.07, font, text_color, background_label_color, 25, 14)

        #make mood image and health bar
        mood_image = ctk.CTkImage(Image.open(mood_imgs[pet_stats["mood"]]),size=(22,22))
        self.mood_image = ctk.CTkLabel(self.app, image=mood_image, text="", bg_color=background_label_color,)
        self.mood_image.place(relx=0.85, rely=0.120, anchor="center")
        self.health_bar = ctk.CTkProgressBar(self.app, width=100, height=10, corner_radius=0, 
                                        fg_color=button_color, progress_color="dark green")
        self.health_bar.pack(padx=0, pady=0)
        self.health_bar.set(pet_stats["health"] / 100)  # Convert health to 0-1 range
        self.health_bar.place(relx=0.435, rely=0.125, anchor="center")

        # Make buttons Settings, Random Event, Sleep, Dance, Feed
        self.make_buttons(self.controller.save_game, 0.17, 0.1025, bg_imgs[0], 1, 35)
        buttons_cmds = [self.controller.random_event, self.controller.sleep, self.controller.dance, self.controller.feed]
        for i in range(4):
            relx = 0.17 + (i * 0.22)
            self.make_buttons(buttons_cmds[i], relx, 0.906, button_imgs[i], 2, 35)

    def make_buttons(self, cmd, relx, rely, image_path=None, border=None, size=None):
        button_image = ctk.CTkImage(Image.open(image_path), size=(size, size))
        button = ctk.CTkButton(self.app,text="", width=size, height=size,corner_radius=0,
                                fg_color=button_color, hover_color=button_hover_color,border_width=border,
                                border_color=button_border_color,command=cmd,image=button_image)
        button.place(relx=relx, rely=rely, anchor="center")
        return button

    def make_labels(self, text, relx, rely, font, text_color, bg_color, width, height):
        label = ctk.CTkLabel(self.app, text=text, font=font, text_color=text_color, bg_color=bg_color,
                             width=width, height=height)
        label.place(relx=relx, rely=rely, anchor="center")
        return label
    
    def update_view(self):
        pet_stats = self.controller.get_pet()
        self.name.configure(text=pet_stats["name"])
        self.age.configure(text=f"Yrs:{pet_stats['age']}")
        self.weight.configure(text=f"Lbs:{pet_stats['weight']}")
        mood_image = ctk.CTkImage(Image.open(mood_imgs[pet_stats["mood"]]), size=(22,22))
        self.mood_image.configure(image=mood_image)
        self.health_bar.set(pet_stats["health"] / 100)
        self.sprite_animator.set_action(pet_stats["action"], pet_stats["background"]) 