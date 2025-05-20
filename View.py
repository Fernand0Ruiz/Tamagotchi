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
    "Assets/Moods/mood_dead.png"
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
        self.tamagotchi = Model()
        self.controller = Controller(self.tamagotchi, self.app)
        self.tamagotchi.add_observer(self.update_view)
        self.name = None
        self.age = None
        self.weight = None
        self.mood_image = None
        self.health_bar = None
        self.sprite_animator = None
        # Store button references
        self.action_buttons = []
        self.game_started = False
        self.ui_initialized = False  # Add flag to track UI initialization
        self.create_app()
        self.show_start_menu()

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

    def show_start_menu(self):
        """Show the start menu before the game begins"""
        # Create start menu frame
        start_frame = ctk.CTkFrame(
            self.app,
            fg_color=background_label_color
        )
        start_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
        
        # Add decorative border frame
        border_frame = ctk.CTkFrame(
            start_frame,
            fg_color=button_border_color,
            corner_radius=0,
            width=280,
            height=360
        )
        border_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Add inner frame with background color
        inner_frame = ctk.CTkFrame(
            border_frame,
            fg_color=background_label_color,
            corner_radius=0,
            width=270,
            height=350
        )
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Add small logo box at the top
        logo_frame = ctk.CTkFrame(
            inner_frame,
            fg_color=button_color,
            corner_radius=0,
            width=70,
            height=70
        )
        logo_frame.place(relx=0.5, rely=0.11, anchor="center")
        
        # Add logo in the box
        logo_image = ctk.CTkImage(Image.open(bg_imgs[0]), size=(60, 60))
        logo_label = ctk.CTkLabel(
            logo_frame,
            image=logo_image,
            text="",
            bg_color=button_color
        )
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Add title with decorative line
        title_frame = ctk.CTkFrame(
            inner_frame,
            fg_color=button_border_color,
            corner_radius=0,
            width=200,
            height=2
        )
        title_frame.place(relx=0.5, rely=0.24, anchor="center")
        
        title_label = ctk.CTkLabel(
            inner_frame,
            text="TAMAGOTCHI",
            font=("Andale Mono", 18, "bold"),
            text_color=text_color,
            bg_color=background_label_color
        )
        title_label.place(relx=0.5, rely=0.24, anchor="center")
        
        # Add instructions text in a frame
        instructions_frame = ctk.CTkFrame(
            inner_frame,
            fg_color=button_color,
            corner_radius=0,
            width=270,
            height=210
        )
        instructions_frame.place(relx=0.5, rely=0.58, anchor="center")
        
        instructions = (
        "HOW TO PLAY\n\n"
        "Interact with your pet using the buttons below!\n"
        "Each action influences its stats,\n"
        "sometimes with a bit of luck.\n\n"
        "CONTROLS\n"
        "FEED — +Weight, +Health.\n"
        "DANCE — -Weight, +Health, -Poop.\n"
        "SLEEP — +Health, +Poop, +Scenery.\n"
        "DICE ROLL — Random effect based on pet's reaction\n"
        "to a scenery change.\n"
        "CLICK POOP — Clean up after your pet or -Health \n"
        "LOGO ICON — ACCESS SETTINGS\n"
        "AUTO-SAVE and Pet Updates every 10 seconds\n"
        "KEEP YOUR PET HAPPY & HEALTHY!\n\n"
        "PRESS START TO BEGIN YOUR ADVENTURE!"
        )
        
        instructions_label = ctk.CTkLabel(
            instructions_frame,
            text=instructions,
            font=("Andale Mono", 9.25, "bold"),
            text_color=text_color,
            justify="left",
            bg_color=button_color,
            width=220,
            height=160,
            corner_radius=0,
            anchor="w"
        )
        instructions_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Add start button
        start_button = ctk.CTkButton(
            inner_frame,
            text="START",
            command=lambda: self.start_game(start_frame),
            width=100,
            height=35,
            corner_radius=0,
            text_color=text_color,
            fg_color=button_color,
            hover_color=button_hover_color,
            border_width=3,
            border_color=button_border_color,
            font=("Andale Mono", 14, "bold")
        )
        start_button.place(relx=0.5, rely=0.91, anchor="center")

    def start_game(self, start_frame):
        """Start the game and remove the start menu"""
        self.game_started = True
        start_frame.destroy()
        self.create_game_ui()
        self.update_view()

    def create_game_ui(self):
        """Create the main game UI elements"""
        # Get pet stats from the controller
        pet_stats = self.controller.get_pet()

        #make sprite animator
        self.sprite_animator = SpriteAnimator(self.app, action=pet_stats["action"], background=pet_stats["background"])
        self.sprite_animator.place(relx=0.5, rely=0.505, anchor="center")
        
        # Add click handler for poop
        self.sprite_animator.bind("<<SpriteClick>>", self.handle_poop_click)

        #make labels
        self.name = self.make_labels(pet_stats["name"], 0.43, 0.08, ("Andale Mono", 14), text_color, background_label_color, 100, 14)  
        self.age = self.make_labels(f"Yrs:{pet_stats['age']}", 0.6725, 0.08, font, text_color, background_label_color, 25, 14)
        self.weight = self.make_labels(f"Lbs:{pet_stats['weight']}", 0.695, 0.124, font, text_color, background_label_color, 25, 14)

        #make mood image and health bar
        mood_image = ctk.CTkImage(Image.open(mood_imgs[pet_stats["mood"]]),size=(30,30))
        self.mood_image = ctk.CTkLabel(self.app, image=mood_image, text="", bg_color=background_label_color,)
        self.mood_image.place(relx=0.85, rely=0.105, anchor="center")
        self.health_bar = ctk.CTkProgressBar(self.app, width=100, height=10, corner_radius=0, 
                                        fg_color=button_color, progress_color="dark green")
        self.health_bar.pack(padx=0, pady=0)
        self.health_bar.set(pet_stats["health"] / 100)  # Convert health to 0-1 range
        self.health_bar.place(relx=0.435, rely=0.125, anchor="center")

        # Make buttons Settings, Random Event, Sleep, Dance, Feed
        self.make_buttons(self.settings_window, 0.17, 0.1025, bg_imgs[0], 1, 35)
        buttons_cmds = [self.controller.random_event, self.controller.sleep, self.controller.dance, self.controller.feed]
        for i in range(4):
            relx = 0.17 + (i * 0.22)
            button = self.make_buttons(buttons_cmds[i], relx, 0.906, button_imgs[i], 2, 35)
            self.action_buttons.append(button)
            
        self.ui_initialized = True  # Set flag after UI is created

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
        if not self.ui_initialized:  # Only update if UI is initialized
            return
        pet_stats = self.controller.get_pet()
        self.name.configure(text=pet_stats["name"])
        self.age.configure(text=f"Yrs:{pet_stats['age']}")
        self.weight.configure(text=f"Lbs:{pet_stats['weight']}")
        mood_image = ctk.CTkImage(Image.open(mood_imgs[pet_stats["mood"]]), size=(30,30))
        self.mood_image.configure(image=mood_image)
        self.health_bar.set(pet_stats["health"] / 100)
        
        #check if tamagotchi is dead or alive 
        if self.tamagotchi.get_is_alive() == False:
            for button in self.action_buttons:
                self.sprite_animator.set_action("dead", pet_stats["background"], self.tamagotchi.get_secondary_action())
                button.configure(state="disabled", fg_color="light gray")
        else:
            # Get the current secondary action
            secondary_action = self.tamagotchi.get_secondary_action()
            
            # Only show poop if there's no other active secondary action
            if self.tamagotchi.get_poop_visible() and not secondary_action:
                secondary_action = "poop"
                
            self.sprite_animator.set_action(pet_stats["action"], pet_stats["background"], secondary_action)
            for button in self.action_buttons:
                button.configure(state="normal", fg_color=button_color)

    def settings_window(self):
        settings_window = ctk.CTkToplevel(self.app)
        settings_window.geometry("200x150")
        settings_window.title("Settings")
        settings_window.resizable(False, False) 
        my_image = ctk.CTkImage(Image.open(bg_imgs[0]), size=(200,150))
        image_label = ctk.CTkLabel(settings_window, image=my_image, text="")
        image_label.pack(padx=0, pady=0)

        self.make_settings_buttons("New Game", 0.5, 0.2, settings_window, lambda: [self.controller.reset_game(), self.update_view(), settings_window.destroy()])
        self.make_settings_buttons("Save Game", 0.5, 0.5, settings_window, lambda: [self.controller.save_game(), self.update_view(), settings_window.destroy()])
        self.make_settings_buttons("Change Name", 0.5, 0.8, settings_window, lambda: [self.show_name_dialog(), settings_window.destroy()])

        # Make the settings window modal
        settings_window.transient(self.app)
        settings_window.grab_set()

    def make_settings_buttons(self, text, relx, rely, settings_window, lambda_cmd):
        new_game_button = ctk.CTkButton(
            settings_window, 
            text=text, 
            command=lambda_cmd,
            width=150, 
            height=35, 
            corner_radius=0, 
            text_color=text_color,
            fg_color=button_color, 
            hover_color=button_hover_color, 
            border_width=3, 
            border_color=button_border_color
        )
        new_game_button.place(relx=relx, rely=rely, anchor="center")

    def show_name_dialog(self):
        dialog = ctk.CTkInputDialog(
            text="Enter new name:",
            title="Change Name"
        )
        new_name = dialog.get_input()
        if new_name:
            self.tamagotchi.set_name(new_name)

    def handle_poop_click(self, event):
        """Handle clicks on the sprite area to clean up poop"""
        print("Poop click detected!")  # Debug print
        if self.controller.clean_poop():
            print("Poop cleaned!")  # Debug print
            self.update_view()
