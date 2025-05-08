import tkinter as tk
from PIL import Image, ImageTk

# Sprite sheet and frame info
SPRITE_SHEET = "Assets/sekitoritchi.png"
FRAME_WIDTH = 64
FRAME_HEIGHT = 64

# Each action: (row, start_frame, frame_count)
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
ACTION_LIST = list(ACTION_MAP.keys())

class SpriteAnimator(tk.Tk):
    def __init__(self, app):
        super().__init__()
        self.title("Sekitoritchi Animation Example")
        self.sprite_sheet = Image.open(SPRITE_SHEET)
        self.current_action_index = 0
        self.current_action = ACTION_LIST[self.current_action_index]
        self.frames = self.load_frames(self.current_action)
        self.current_frame = 0

        self.label = tk.Label(app, width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.label.pack()

        self.animate()

    def load_frames(self, action):
        frames = []
        row, start, count = ACTION_MAP[action]
        for i in range(start, start + count):
            left = i * FRAME_WIDTH
            upper = row * FRAME_HEIGHT
            right = left + FRAME_WIDTH
            lower = upper + FRAME_HEIGHT
            frame = self.sprite_sheet.crop((left, upper, right, lower))
            frames.append(ImageTk.PhotoImage(frame))
        return frames

    def animate(self):
        self.label.config(image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.after(300, self.animate)

    def set_action(self, action):
        if action in ACTION_MAP:
            self.current_action = action
            self.frames = self.load_frames(action)
            self.current_frame = 0