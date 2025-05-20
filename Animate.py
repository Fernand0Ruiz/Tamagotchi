import tkinter as tk
from PIL import Image, ImageTk

# Sprite sheet and frame info
SPRITE_SHEET = "Assets/sprite.png"  # Path to the sprite sheet containing all animations
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
    "Assets/Weather/night.png",
    "Assets/Weather/outside.png",
    "Assets/Weather/sunset_outside.png",
    "Assets/Weather/night_outside.png"
]

# Animation frame mapping for each action
# Format: "action_name": (row, start_frame, frame_count)
# - row: which row in the sprite sheet contains this animation
# - start_frame: which frame number in that row the animation starts at
# - frame_count: how many frames are in this animation
ACTION_MAP = {
    "happy":  (0, 0, 4),  # 4 frames starting at frame 0 in row 0
    "middle": (0, 0, 2),    # 4 frames starting at frame 4 in row 0
    "sad": (0, 4, 4),    # 4 frames starting at frame 4 in row 0
    "dance": (0, 8, 4),  # 4 frames starting at frame 8 in row 0
    "sleep": (1, 0, 4),  # 4 frames starting at frame 0 in row 1
    "angry": (1, 4, 4),  # 4 frames starting at frame 4 in row 1
    "oniguri": (1, 8, 4), # 4 frames starting at frame 8 in row 1
    "fustrated":(2, 0, 10), # 10 frames starting at frame 0 in row 2
    "eat":(3, 0, 4),     # 4 frames starting at frame 0 in row 3
    "dead":(3, 4, 4),    # 4 frames starting at frame 4 in row 3
    "dessert":(3, 8, 4), # 4 frames starting at frame 8 in row 3
    "pooping":(4, 0, 4),  # 4 frames starting at frame 0 in row 4
    "dance_reverse":(4, 4, 4), # 4 frames starting at frame 4 in row 4
    "attention":(5, 0, 4), # 4 frames starting at frame 0 in row 5
    "look":(5, 4, 4),     # 4 frames starting at frame 4 in row 5
    "poop":(5, 8, 1)     # 4 frames starting at frame 0 in row 6
}
ACTION_LIST = list(ACTION_MAP.keys())  # List of all available actions

class SpriteAnimator(tk.Frame):
    """
    A class that handles sprite animation using a sprite sheet.
    This class manages the animation of the Tamagotchi character by:
    1. Loading frames from a sprite sheet
    2. Combining them with background images
    3. Displaying them in sequence to create animations
    4. Handling transitions between different actions
    """
    def __init__(self, parent, action="idle", background=None, secondary_action=None, secondary_action_position="left"):
        """
        Initialize the SpriteAnimator.
        
        Args:
            parent: The parent tkinter widget where the animation will be displayed
            action: The initial animation to play (defaults to "idle")
            background: The index of the background image to use (optional)
            secondary_action: Optional secondary action to composite alongside the main action
            secondary_action_position: Position of secondary action ("left" or "right")
        """
        super().__init__(parent)
        # Load the main sprite sheet containing all animations
        self.sprite_sheet = Image.open(SPRITE_SHEET)
        
        # Set up background if provided
        self.background_index = background
        if background is not None:
            self.background = Image.open(Weather_imgs[background])
            self.background = self.background.resize((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
        else:
            self.background = None
            
        # Initialize animation state
        self.action = action
        self.secondary_action = secondary_action
        self.secondary_action_position = secondary_action_position
        self.frames = self.load_frames(action, secondary_action)
        self.current_frame = 0
        
        # Create and set up the label that will display the animation
        self.label = tk.Label(self)
        self.label.pack(expand=True, fill='both')
        
        # Make the label clickable
        self.label.bind("<Button-1>", self.on_click)
        
        # Start the animation loop
        self.animate()
        
        # Preload common actions for smoother transitions
        self.preloaded_frames = {}
        self.preload_common_actions()

    def preload_common_actions(self):
        """
        Preload frames for common actions to make transitions smoother.
        This prevents the black screen flash when switching between frequent actions.
        """
        # Don't preload frames as they need to be created with the current background
        pass

    def load_frames(self, action, secondary_action=None):
        """
        Load all frames for a specific action from the sprite sheet.
        
        Args:
            action: The name of the action to load frames for
            secondary_action: Optional secondary action to composite alongside the main action
            
        Returns:
            list: A list of PhotoImage objects containing each frame of the animation
        """
        frames = []
        # Get the frame information for this action
        row, start, count = ACTION_MAP[action]
        
        # Get secondary action info if provided
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
        
        # Extract each frame from the sprite sheet
        for i in range(start, start + count):
            # Calculate the position of this frame in the sprite sheet
            left = i * ORIGINAL_FRAME_WIDTH
            upper = row * ORIGINAL_FRAME_HEIGHT
            right = left + ORIGINAL_FRAME_WIDTH
            lower = upper + ORIGINAL_FRAME_HEIGHT
            
            # Extract and resize the frame
            frame = self.sprite_sheet.crop((left, upper, right, lower))
            frame = frame.resize((FRAME_WIDTH, FRAME_HEIGHT), Image.Resampling.LANCZOS)
            
            if self.background:
                # Create a new image with the background
                composite = self.background.copy()
                
                # Ensure the frame has transparency
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                    
                # Calculate position to center the sprite on the background
                x = (BACKGROUND_WIDTH - FRAME_WIDTH) // 2
                y = (BACKGROUND_HEIGHT - FRAME_HEIGHT) // 2 + SPRITE_Y_OFFSET
                
                # Combine the frame with the background
                composite.paste(frame, (x, y), frame.split()[3])
                
                # Add secondary action if provided
                if secondary_frames:
                    sec_frame = secondary_frames[i % len(secondary_frames)]
                    # Hardcode positioning based on secondary action type
                    if self.secondary_action == "poop":
                        sec_x = x + FRAME_WIDTH - 20  # Position poop on the right
                    else:
                        sec_x = x - FRAME_WIDTH + 20  # Position everything else (eating) on the left
                    sec_y = y  # Same vertical position as main sprite
                    composite.paste(sec_frame, (sec_x, sec_y+10), sec_frame.split()[3])
                
                frames.append(ImageTk.PhotoImage(composite))
            else:
                # If no background, just use the frame
                frames.append(ImageTk.PhotoImage(frame))
        
        return frames

    def animate(self):
        """
        Animate the sprite by cycling through frames.
        This method is called repeatedly to create the animation effect.
        It updates the display every 100 milliseconds for smoother animation.
        """
        if self.frames:  # Only update if we have frames
            # Update the label with the current frame
            self.label.config(image=self.frames[self.current_frame])
            # Move to the next frame, looping back to 0 if we reach the end
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        # Schedule the next frame update
        self.after(100, self.animate)  # Reduced from 300ms to 100ms for smoother animation

    def set_action(self, action, background, secondary_action=None, secondary_action_position="left"):
        """
        Change the current animation to a different action.
        This method handles the transition between different animations
        while trying to prevent any visual glitches.
        
        Args:
            action: The name of the new action to play
            background: The index of the new background to use
            secondary_action: Optional secondary action to composite alongside the main action
            secondary_action_position: Position of secondary action ("left" or "right")
        """
        # Keep current frame visible during transition
        current_image = self.frames[self.current_frame] if self.frames else None
        self.label.config(image=current_image)
        self.label.update()
        
        # Update background if it has changed
        if self.background is None or background != self.background_index:
            self.background = Image.open(Weather_imgs[background])
            self.background = self.background.resize((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
            self.background_index = background
        
        # Update action if it has changed
        if action != self.action and action in ACTION_MAP:
            self.action = action
            
        # Update secondary action if provided
        if secondary_action != self.secondary_action:
            self.secondary_action = secondary_action
            
        # Update secondary action position
        self.secondary_action_position = secondary_action_position
        
        # Always reload frames to ensure they have the current background
        self.frames = self.load_frames(self.action, self.secondary_action)
        self.current_frame = 0
        
        # Ensure smooth transition to new animation
        if self.frames:
            self.label.config(image=self.frames[self.current_frame])
            self.label.update()

    def on_click(self, event):
        """Handle click events on the sprite"""
        # Forward the click event to the parent
        self.event_generate("<<SpriteClick>>")