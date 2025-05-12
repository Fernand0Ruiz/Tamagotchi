import tkinter as tk
from PIL import Image, ImageTk
import os

# Sprite sheet and frame info
SPRITE_SHEET = "Assets/sekitoritchi.png"  # Path to the sprite sheet containing all animations
FRAME_WIDTH = 75  # Width of each sprite frame in pixels
FRAME_HEIGHT = 75  # Height of each sprite frame in pixels
BACKGROUND_WIDTH = 300  # Width of the background image
BACKGROUND_HEIGHT = 250  # Height of the background image
SPRITE_Y_OFFSET = 60  # Vertical offset to move sprite down from center
ORIGINAL_FRAME_WIDTH = 64  # Original size of sprites in the sprite sheet
ORIGINAL_FRAME_HEIGHT = 64  # Original size of sprites in the sprite sheet

# Weather background images for different states
Weather_imgs = [
    "Assets/Weather/morning.png",
    "Assets/Weather/heavenly.png",
    "Assets/Weather/rainy.png",
    "Assets/Weather/sunset.png",
    "Assets/Weather/night.png"
]

# Animation frame mapping for each action
# Format: "action_name": (row, start_frame, frame_count)
# - row: which row in the sprite sheet contains this animation
# - start_frame: which frame number in that row the animation starts at
# - frame_count: how many frames are in this animation
ACTION_MAP = {
    "idle":  (0, 0, 4),
    "cry": (0, 4, 4),
    "dance": (0, 8, 4),
    "sleep": (1, 0, 4),
    "angry": (1, 4, 4),
    "oniguri": (1, 8, 4),
    "fustrated":(2, 0, 10),
    "eat":(3, 0, 4),
    "dead":(3, 4, 4),
    "dessert":(3, 8, 4),
    "peeing":(4, 0, 4),
    "dance_reverse":(4, 4, 4),
    "attention":(5, 0, 4),
    "poop":(5, 4, 4)     
}
ACTION_LIST = list(ACTION_MAP.keys())  # List of all available actions

class SpriteAnimator:
    def __init__(self, parent, action="idle", background=0):
        # Initialize animation properties
        self.parent = parent
        self.current_frame = 0
        self.frames = []
        self.animation_running = False
        self.current_action = action
        self.current_background = background
        
        # Create label for displaying frames
        self.label = tk.Label(parent, bg="white")
        self.label.pack()
        
        # Load initial frames
        self.load_frames(action, background)
        
        # Start animation loop
        self.animate()

    def load_frames(self, action, background):
        """Load animation frames for given action and background"""
        self.frames = []
        base_path = f"Assets/Sprites/{action}"
        
        # Load each frame in the sequence
        for i in range(4):  # Assuming 4 frames per animation
            try:
                frame_path = f"{base_path}/{i}.png"
                if os.path.exists(frame_path):
                    frame = Image.open(frame_path)
                    self.frames.append(ImageTk.PhotoImage(frame))
            except Exception as e:
                print(f"Error loading frame {i} for {action}: {e}")

    def set_action(self, action, background):
        """Update current animation and background"""
        if action != self.current_action or background != self.current_background:
            self.current_action = action
            self.current_background = background
            self.load_frames(action, background)
            self.current_frame = 0

    def animate(self):
        """Update animation frame"""
        if self.frames:
            self.label.configure(image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.parent.after(100, self.animate)  # Update every 100ms

    def place(self, **kwargs):
        """Position the sprite animator"""
        self.label.place(**kwargs)