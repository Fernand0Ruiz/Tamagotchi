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
    MOOD_DEAD = 4
    def __init__(self):
        self.data_manager = DataManager()
        self._observers = []  # List to store observer callbacks
        self.load_game_state()
        self.is_running = True
        self.is_updating = False
        self.secondary_action = None  # Initialize secondary_action
        self.poop_visible = False  # Track if poop is currently visible

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
        self.action = self.get_action_mood()
        self.background = data["background"]
        self.poop_level = data["poop_level"]
        self.poop_visible = False  # Reset poop visibility on load

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
    
    def reset_game(self):
        self.data_manager.reset_data()
        self.load_game_state()


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

    def get_secondary_action(self):
        """Get the current secondary action of the pet"""
        return self.secondary_action

    def get_background(self) -> str:
        return self.background
    
    def get_poop_level(self) -> int:
        return self.poop_level
    
    def get_poop_visible(self):
        """Get whether poop is currently visible"""
        return self.poop_visible

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

    def set_action(self, action, secondary_action=None):
        """Set the current action of the pet"""
        self.action = action
        self.secondary_action = secondary_action
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

    def set_poop_visible(self, visible):
        """Set whether poop is currently visible"""
        self.poop_visible = visible
        self._notify_observers()

    def should_trigger_poop_animation(self):
        """Check if poop animation should be triggered"""
        print(f"Checking poop trigger - level: {self.poop_level}")  # Debug print
        if self.poop_level >= 75:
            print("Poop level threshold reached!")  # Debug print
            self.poop = True
            self.poop_visible = True  # Set poop as visible
            # Poop affects health negatively
            self.health = max(0, self.health - 3)
            return True
        return False

    def update_stats(self):
        """Update pet stats over time"""
        if not self.is_running or not self.is_alive or self.is_updating:
            return

        try:
            self.is_updating = True  # Acquire lock
            
            # Calculate base decrease based on current stats
            base_decrease = random.randint(1, 2)  # Reduced from 1-5 to 1-2
            
            # Apply health and weight changes with condition adjustments
            if self.weight > 350:
                # Overweight pets lose health faster
                self.health = max(0, self.health - base_decrease)  # Reduced from base_decrease * 2
                self.weight = max(0, self.weight - (base_decrease // 2))  # Reduced from base_decrease
            elif self.age > 50:
                # Older pets lose health faster
                self.health = max(0, self.health - base_decrease)  # Reduced from int(base_decrease * 1.5)
                self.weight = max(0, self.weight - (base_decrease // 3))  # Reduced from base_decrease // 2
            else:
                # Normal decrease
                self.health = max(0, self.health - (base_decrease // 2))  # Reduced from base_decrease
                self.weight = max(0, self.weight - (base_decrease // 4))  # Reduced from base_decrease // 2

            # Decrease health if poop is visible
            if self.poop_visible:
                self.health = max(0, self.health - 3)

            # Increase poop level more gradually
            self.poop_level = min(100, self.poop_level + 5)  # Reduced from 10 to 5
            print(f"Current poop level: {self.poop_level}")  # Debug print
            
            # Increment age
            self.age += 1
            
            # Check if pet is still alive first
            if self.health <= 0 or self.weight <= 0:
                self.is_alive = False
                self.mood = self.MOOD_DEAD
                self.action = "dead"
            # Update mood based on health ranges with hysteresis
            elif 75 <= self.health <= 100:
                self.action = "happy"
                self.mood = self.MOOD_HAPPY
            elif 50 <= self.health < 75:
                self.action = "middle"
                self.mood = self.MOOD_MIDDLE
            elif 25 <= self.health < 50:
                self.action = "angry"
                self.mood = self.MOOD_ANGRY
            else:
                self.action = "sad"
                self.mood = self.MOOD_SAD

            self.save_game_state()
            self._notify_observers()
            
        except tk.TclError:
            self.is_running = False
        finally:
            self.is_updating = False  # Release lock

    def stop(self):
        """Stop the model and cleanup"""
        self.is_running = False

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
        
    def reset_data(self):
        self.save_data(self.default_data)