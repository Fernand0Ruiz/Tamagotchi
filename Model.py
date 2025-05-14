import json
import os
import time
import tkinter as tk
from datetime import datetime
import random

class Model:
    MOOD_HAPPY = 0
    MOOD_MIDDLE = 1
    MOOD_ANGRY = 2
    MOOD_SAD = 3

    def __init__(self, main_window=None):
        self.data_manager = DataManager()
        self._observers = []  # List to store observer callbacks
        self.load_game_state()
        self.update_interval = 30  # Update stats every 30 seconds
        self.is_running = True
        self.main_window = main_window
        self.is_updating = False
        
        # Start the timer if we have a main window
        if self.main_window:
            self.schedule_next_update()

    def add_observer(self, callback):
        """Add an observer callback function"""
        if callback not in self._observers:
            self._observers.append(callback)
    
    def remove_observer(self, callback):
        """Remove an observer callback function"""
        if callback in self._observers:
            self._observers.remove(callback)
    
    def _notify_observers(self):
        """Notify all observers of a change"""
        if not self.is_running:
            return
        for observer in self._observers:
            try:
                observer()
            except tk.TclError:
                # If we get a TclError, the window was probably destroyed
                self.is_running = False
                break

    def load_game_state(self):
        """Load the game state from saved data"""
        data = self.data_manager.load_data()
        self.name = data["name"]
        self.age = data["age"]
        self.weight = data["weight"]
        self.mood = data["mood"]
        self.health = data["health"]
        self.poop = data["poop"]
        self.is_alive = data["alive"]
        self.action = data["action"]
        self.background = data["background"]
        self.poop_level = data["poop_level"]

    def save_game_state(self):
        """Save the current game state"""
        data = {
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "mood": self.mood,
            "health": self.health,
            "poop": self.poop,
            "poop_level": self.poop_level,
            "alive": self.is_alive,
            "action": self.action,
            "background": self.background
        }
        return self.data_manager.save_data(data)

    def get_name(self) -> str:
        return self.name
    
    def get_age(self) -> int:
        return self.age
    
    def get_health(self) -> int:
        return self.health
    
    def get_is_alive(self) -> bool:
        return self.is_alive
    
    def get_poop(self) -> int:
        return self.poop 

    def get_weight(self) -> int:
        return self.weight
    
    def get_mood(self) -> int:
        return self.mood
    
    def get_action_mood(self) -> str:
        if self.mood == self.MOOD_HAPPY:
            return "happy"
        elif self.mood == self.MOOD_MIDDLE:
            return "middle"
        elif self.mood == self.MOOD_ANGRY:
            return "angry"
        else:
            return "sad"
        
    def get_action(self) -> str:
        return self.action 

    def get_background(self) -> str:
        return self.background
    
    def get_poop_level(self) -> int:
        return self.poop_level
    
    def set_name(self,name: str):
        self.name = name
        self._notify_observers()

    def set_age(self, age: int):
        self.age = age
        self._notify_observers()

    def set_health(self, health: int):
        self.health = max(0, min(100, health))  # Clamp health between 0 and 100
        self._notify_observers()

    def set_is_alive(self,alive: bool):
        self.is_alive = alive
        self._notify_observers()

    def set_poop(self, poop: int):
        self.poop = poop
        self._notify_observers()

    def set_action(self, action: str):
        self.action = action
        self._notify_observers()
    
    def set_background(self, background: int):
        self.background = background
        self._notify_observers()

    def set_weight(self, weight: int):
        self.weight = weight
        self._notify_observers()

    def set_poop_level(self, poop_level: int):
        self.poop_level = poop_level
        self._notify_observers()

    def schedule_next_update(self):
        """Schedule the next stats update"""
        if not self.is_running or not self.main_window:
            return
        try:
            self.main_window.after(self.update_interval * 1000, self.update_stats)
        except tk.TclError:
            self.is_running = False

    def update_stats(self):
        """Update pet stats over time"""
        if not self.is_running or not self.is_alive or self.is_updating:
            return

        try:
            self.is_updating = True  # Acquire lock
            # Calculate base decrease based on current stats
            base_decrease = random.randint(1, 5)
            
            # Apply health and weight changes with condition adjustments
            if self.weight > 350:
                # Overweight pets lose health faster
                self.health = max(0, self.health - (base_decrease * 2))
                self.weight = max(0, self.weight - base_decrease)
            elif self.age > 50:
                # Older pets lose health faster
                self.health = max(0, self.health - int(base_decrease * 1.5))
                self.weight = max(0, self.weight - (base_decrease // 2))
            else:
                # Normal decrease
                self.health = max(0, self.health - base_decrease)
                self.weight = max(0, self.weight - (base_decrease // 2))

            # Increase poop level more gradually
            self.poop_level = min(100, self.poop_level + (base_decrease // 2))
            
            # Increment age
            self.age += 1
            
            # Check if pet is still alive first
            if self.health <= 0 or self.weight <= 0:
                self.is_alive = False
                self.mood = self.MOOD_SAD
                self.action = "dead"
            # Update mood based on health with more granular ranges
            elif self.health >= 75:
                self.mood = self.MOOD_HAPPY
                self.action = "happy"
            elif self.health >= 60:
                self.mood = self.MOOD_MIDDLE
                self.action = "middle"
            elif self.health >= 30:
                self.mood = self.MOOD_ANGRY
                self.action = "angry"
            else:
                self.mood = self.MOOD_SAD
                self.action = "sad"

            # Handle poop state
            if self.poop_level >= 75:
                self.poop_level = 0
                self.poop = True
                # Poop affects health negatively
                self.health = max(0, self.health - 3)

            self.save_game_state()
            self._notify_observers()
            
            # Schedule next update if still running
            if self.is_running:
                self.schedule_next_update()
        except tk.TclError:
            self.is_running = False
        finally:
            self.is_updating = False  # Release lock

    def stop(self):
        """Stop the model and cleanup"""
        self.is_running = False
        self.main_window = None

    def __del__(self):
        """Cleanup when the model is destroyed"""
        self.stop()

class DataManager:
    def __init__(self):
        self.save_file = "tamagotchi_save.json"
        self.default_data = {
            "name": "Sekitoritchi",
            "age": 1,
            "weight": 250,
            "mood": 0,
            "health": 100,
            "poop": False,  
            "poop_level": 0,
            "alive": True,
            "action": "happy",
            "background": 0
        }

    def save_data(self, data):
        """Save game data to JSON file"""
        try:
            with open(self.save_file, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def load_data(self):
        """Load game data from JSON file"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    return json.load(f)
            return self.default_data
        except Exception as e:
            print(f"Error loading data: {e}")
            return self.default_data 