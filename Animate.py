"""
Sprite Animation System for Tamagotchi Game
Handles sprite animations, backgrounds, and interactions.
"""

import tkinter as tk
from PIL import Image, ImageTk

# Sprite sheet configuration
SPRITE_SHEET = "Assets/sprite.png"
FRAME_WIDTH = 75
FRAME_HEIGHT = 75
BACKGROUND_WIDTH = 300
BACKGROUND_HEIGHT = 250
SPRITE_Y_OFFSET = 60
ORIGINAL_FRAME_WIDTH = 64
ORIGINAL_FRAME_HEIGHT = 64

# Weather background images
Weather_imgs = [
    "Assets/Weather/morning.png",      # Morning scene
    "Assets/Weather/heavenly.png",     # Clear day
    "Assets/Weather/rainy.png",        # Rainy weather
    "Assets/Weather/sunset.png",       # Sunset indoors
    "Assets/Weather/night.png",        # Night indoors
    "Assets/Weather/outside.png",      # Day outdoors
    "Assets/Weather/sunset_outside.png",# Sunset outdoors
    "Assets/Weather/night_outside.png"  # Night outdoors
]

# Animation frame mapping: (row, start_frame, frame_count)
ACTION_MAP = {
    "happy":  (0, 0, 4),    
    "middle": (0, 0, 2),    
    "sad":    (0, 4, 4),    
    "dance":  (0, 8, 4),    
    "sleep":  (1, 0, 4),    
    "angry":  (1, 4, 4),    
    "oniguri":(1, 8, 4),    
    "fustrated":(2, 0, 10), 
    "eat":    (3, 0, 4),    
    "dead":   (3, 4, 4),    
    "dessert":(3, 8, 4),    
    "pooping":(4, 0, 4),    
    "dance_reverse":(4, 4, 4), 
    "attention":(5, 0, 4), 
    "look":   (5, 4, 4),    
    "poop":   (5, 8, 1)     
}
ACTION_LIST = list(ACTION_MAP.keys())

class SpriteAnimator(tk.Frame):
    """Handles sprite animation using a sprite sheet."""
    def __init__(self, parent, action="idle", background=None, secondary_action=None):
        """Initialize the SpriteAnimator."""
        super().__init__(parent)
        self.sprite_sheet = Image.open(SPRITE_SHEET)
        
        self.background_index = background
        if background is not None:
            self.background = Image.open(Weather_imgs[background])
            self.background = self.background.resize((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
        else:
            self.background = None
            
        self.action = action
        self.secondary_action = secondary_action
        self.frames = self.load_frames(action, secondary_action)
        self.current_frame = 0
        
        self.label = tk.Label(self)
        self.label.pack(expand=True, fill='both')
        self.label.bind("<Button-1>", self.on_click)
        
        self.animate()

    def load_frames(self, action, secondary_action=None):
        """Load frames for a specific action from the sprite sheet."""
        frames = []
        row, start, count = ACTION_MAP[action]
        
        secondary_frames = []
        if secondary_action and secondary_action in ACTION_MAP:
            sec_row, sec_start, sec_count = ACTION_MAP[secondary_action]
            for i in range(sec_start, sec_start + sec_count):
                left = i * ORIGINAL_FRAME_WIDTH
                upper = sec_row * ORIGINAL_FRAME_HEIGHT
                right = left + ORIGINAL_FRAME_WIDTH
                lower = upper + ORIGINAL_FRAME_HEIGHT
                frame = self.sprite_sheet.crop((left, upper, right, lower))
                frame = frame.resize((FRAME_WIDTH, FRAME_HEIGHT), Image.Resampling.LANCZOS)
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                secondary_frames.append(frame)
        
        for i in range(start, start + count):
            left = i * ORIGINAL_FRAME_WIDTH
            upper = row * ORIGINAL_FRAME_HEIGHT
            right = left + ORIGINAL_FRAME_WIDTH
            lower = upper + ORIGINAL_FRAME_HEIGHT
            
            frame = self.sprite_sheet.crop((left, upper, right, lower))
            frame = frame.resize((FRAME_WIDTH, FRAME_HEIGHT), Image.Resampling.LANCZOS)
            
            if self.background:
                composite = self.background.copy()
                
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                    
                x = (BACKGROUND_WIDTH - FRAME_WIDTH) // 2
                y = (BACKGROUND_HEIGHT - FRAME_HEIGHT) // 2 + SPRITE_Y_OFFSET
                
                composite.paste(frame, (x, y), frame.split()[3])
                
                if secondary_frames:
                    sec_frame = secondary_frames[i % len(secondary_frames)]
                    if self.secondary_action == "poop":
                        sec_x = x + FRAME_WIDTH - 20
                    else:
                        sec_x = x - FRAME_WIDTH + 20
                    sec_y = y
                    composite.paste(sec_frame, (sec_x, sec_y+10), sec_frame.split()[3])
                
                frames.append(ImageTk.PhotoImage(composite))
            else:
                frames.append(ImageTk.PhotoImage(frame))
        
        return frames

    def animate(self):
        """Animate the sprite by cycling through frames."""
        if self.frames:
            self.label.config(image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.after(100, self.animate)

    def set_action(self, action, background, secondary_action=None):
        """Change the current animation to a different action."""
        current_image = self.frames[self.current_frame] if self.frames else None
        self.label.config(image=current_image)
        self.label.update()
        
        if self.background is None or background != self.background_index:
            self.background = Image.open(Weather_imgs[background])
            self.background = self.background.resize((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
            self.background_index = background
        
        if action != self.action and action in ACTION_MAP:
            self.action = action
            
        if secondary_action != self.secondary_action:
            self.secondary_action = secondary_action
            
        self.frames = self.load_frames(self.action, self.secondary_action)
        self.current_frame = 0
        
        if self.frames:
            self.label.config(image=self.frames[self.current_frame])
            self.label.update()

    def on_click(self, event):
        """Handle click events on the sprite."""
        self.event_generate("<<SpriteClick>>")