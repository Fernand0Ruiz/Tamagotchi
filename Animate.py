"""
Sprite Animation System for Tamagotchi Game
Handles sprite animations, backgrounds, and interactions.
"""

import tkinter as tk
from PIL import Image, ImageTk

# Sprite sheet configuration
SPRITE_SHEET = "Assets/sprite.png"
DISPLAY_FRAME_WIDTH = 75
DISPLAY_FRAME_HEIGHT = 75
BACKGROUND_WIDTH = 300
BACKGROUND_HEIGHT = 250
SPRITE_Y_OFFSET = 60
SPRITE_SHEET_FRAME_WIDTH = 64
SPRITE_SHEET_FRAME_HEIGHT = 64

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

class SpriteAnimator(tk.Frame):
    """Handles sprite animation using a sprite sheet."""
    def __init__(self, parent, action="idle", background=0, secondary_action=None):
        """Initialize the SpriteAnimator."""
        super().__init__(parent)
        self.sprite_sheet = Image.open(SPRITE_SHEET)
        
        # Set background based off saved json file or default to morning
        self.background_index = background
        self.background = Image.open(Weather_imgs[background])
        self.background = self.background.resize((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
            
        self.action = action
        self.secondary_action = secondary_action
        self.frames = self.load_frames(action, secondary_action)
        self.current_frame = 0
        
        self.sprite_display = tk.Label(self)
        self.sprite_display.pack(expand=True, fill='both')
        self.sprite_display.bind("<Button-1>", self.on_click)
        
        self.animate()

    def _ensure_rgba(self, frame):
        """Helper method to ensure frame is in RGBA mode."""
        if frame.mode != 'RGBA':
            return frame.convert('RGBA')
        return frame

    def load_frames(self, action, secondary_action=None):
        """Load frames for a specific action from the sprite sheet."""
        frames = []
        row, start, count = ACTION_MAP[action]
        
        # Handle secondary action frames (like food when eating or poop when pooping)
        secondary_frames = []
        if secondary_action and secondary_action in ACTION_MAP:
            # Get sprite object coordinates on sprite sheet
            sec_row, sec_start, sec_count = ACTION_MAP[secondary_action]
            for i in range(sec_start, sec_start + sec_count):
                # Calculate crop coordinates for sprite sizing and positioning
                left = i * SPRITE_SHEET_FRAME_WIDTH
                upper = sec_row * SPRITE_SHEET_FRAME_HEIGHT
                right = left + SPRITE_SHEET_FRAME_WIDTH
                lower = upper + SPRITE_SHEET_FRAME_HEIGHT
                # Crop and resize the secondary sprite frame
                frame = self.sprite_sheet.crop((left, upper, right, lower))
                frame = frame.resize((DISPLAY_FRAME_WIDTH, DISPLAY_FRAME_HEIGHT), Image.Resampling.LANCZOS)
                secondary_frames.append(self._ensure_rgba(frame))
        
        # Load main action frames
        for i in range(start, start + count):
            # Get sprite object coordinates on sprite sheet
            left = i * SPRITE_SHEET_FRAME_WIDTH
            upper = row * SPRITE_SHEET_FRAME_HEIGHT
            right = left + SPRITE_SHEET_FRAME_WIDTH
            lower = upper + SPRITE_SHEET_FRAME_HEIGHT
            
            # Crop and resize the main sprite frame
            frame = self.sprite_sheet.crop((left, upper, right, lower))
            frame = frame.resize((DISPLAY_FRAME_WIDTH, DISPLAY_FRAME_HEIGHT), Image.Resampling.LANCZOS)
            
            # Create composite image with background
            composite = self.background.copy()
            frame = self._ensure_rgba(frame)
                
            # Calculate center position for the sprite
            x = (BACKGROUND_WIDTH - DISPLAY_FRAME_WIDTH) // 2
            y = (BACKGROUND_HEIGHT - DISPLAY_FRAME_HEIGHT) // 2 + SPRITE_Y_OFFSET
            
            # Paste the main sprite onto the background
            composite.paste(frame, (x, y), frame.split()[3])
            
            # If there's a secondary action, add it to the composite
            if secondary_frames:
                sec_frame = secondary_frames[i % len(secondary_frames)]
                # Position secondary sprite based on type (poop goes to right, food goes to left)
                if self.secondary_action == "poop":
                    sec_x = x + DISPLAY_FRAME_WIDTH - 20
                else:
                    sec_x = x - DISPLAY_FRAME_WIDTH + 20
                sec_y = y
                # Paste the secondary sprite onto the composite
                composite.paste(sec_frame, (sec_x, sec_y+10), sec_frame.split()[3])
            
            # Convert the composite to a Tkinter-compatible image and add to frames list
            frames.append(ImageTk.PhotoImage(composite))
        
        return frames

    def animate(self):
        """Animate the sprite by cycling through frames."""
        if self.frames:
            # Set current frame
            self.sprite_display.config(image=self.frames[self.current_frame])
            # Increment frame index
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        # Cycle through each frame every 100ms
        self.after(100, self.animate)

    def set_action(self, action, background, secondary_action=None):
        """Change the current animation to a different action."""
        current_image = self.frames[self.current_frame] if self.frames else None
        self.sprite_display.config(image=current_image)
        self.sprite_display.update()
        
        # Change background if it is different from the current background
        if background != self.background_index:
            self.background = Image.open(Weather_imgs[background])
            self.background = self.background.resize((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
            self.background_index = background
        
        # Change action if it is different from the current action
        if action != self.action and action in ACTION_MAP:
            self.action = action
            
        # Change secondary action if it is different from the current secondary action
        if secondary_action != self.secondary_action:
            self.secondary_action = secondary_action    
        
        # Load new frames
        self.frames = self.load_frames(self.action, self.secondary_action)
        self.current_frame = 0
        # Set current frame to first frame
        if self.frames:
            self.sprite_display.config(image=self.frames[self.current_frame])
            self.sprite_display.update()

    def on_click(self, event):
        """Handle click events on the sprite."""
        self.event_generate("<<SpriteClick>>")