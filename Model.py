import json
import os
import tkinter as tk
import random

class Model:
    """ Mood constants. """
    MOOD_HAPPY = 0
    MOOD_MIDDLE = 1
    MOOD_ANGRY = 2
    MOOD_SAD = 3
    MOOD_DEAD = 4

    """ Initializes the model. """
    def __init__(self, observer):
        self.data_manager = DataManager()
        self.observer = Observer()  # Create observer instance
        self.observer.add_observer(observer) # Add passed in observer
        self.load_game_state() # Load game state, if none use default values
        self.is_running = True # Track if the model is running
        self.is_updating = False # Track if the model is updating
        self.secondary_action = None  # Initialize secondary_action
        self.poop_visible = False  # Track if poop is currently visible

    """ Loads the game state from saved data. """
    def load_game_state(self):
        data = self.data_manager.load_data()
        self.name = data["name"]
        self.age = data["age"]
        self.weight = data["weight"]
        self.mood = data["mood"]
        self.health = data["health"]
        self.is_alive = data["is_alive"]
        self.action = self.get_action_mood()
        self.background = data["background"]
        self.poop_level = data["poop_level"]
        self.poop_visible = False  # Reset poop visibility on load

    """ Saves the current game state. """
    def save_game_state(self):
        data = self.get_pet()
        return self.data_manager.save_data(data)
    
    """ Resets the game state (with default values) and loads new game state (default values). """
    def reset_game(self):
        self.data_manager.reset_data()
        self.load_game_state()

    """ Stops the model and cleanup. """
    def stop(self):
        self.is_running = False
        self.observer.stop()

    """ Cleans up the model when it is destroyed. """
    def __del__(self):
        self.stop()

    """ Returns the pet's idle action based on mood. """
    def get_action_mood(self) -> str:
        if self.mood == self.MOOD_HAPPY:
            return "happy"
        elif self.mood == self.MOOD_MIDDLE:
            return "middle"
        elif self.mood == self.MOOD_ANGRY:
            return "angry"
        else:
            return "sad"

    """ Returns the pet's secondary action. """
    def get_secondary_action(self) -> str:
        return self.secondary_action

    """ Returns whether the pet is alive. """
    def get_is_alive(self) -> bool:
        return self.is_alive

    """ Returns if poop is visible. Poop visible effects the pet's health. """
    def get_poop_visible(self) -> bool:
        return self.poop_visible
    
    """ Returns the pet's background. """
    def get_background(self) -> int:
        return self.background
    
    """ Returns a dictionary pet stats for view updates. """
    def get_pet(self):
        stats = {}    
        stats["name"] = self.name
        stats["age"] = self.age
        stats["weight"] = self.weight
        stats["mood"] = self.mood
        stats["health"] = self.health
        stats["poop_level"] = self.poop_level
        stats["is_alive"] = self.is_alive
        stats["poop_visible"] = self.poop_visible
        stats["action"] = self.action
        stats["background"] = self.background
        
        return stats

    """ Sets the pet's name. """
    def set_name(self, name: str):
        self.name = name
        self.observer.notify_observers()

    """ Sets the pet's age. """
    def set_age(self, age: int):
        self.age = age
        self.observer.notify_observers()

    """ Sets the pet's health. """
    def set_health(self, health: int):
        # Clamp health between 0 and 100
        self.health = max(0, min(100, health))  
        self.observer.notify_observers()

    """ Sets whether the pet is alive. """
    def set_is_alive(self, alive: bool):
        self.is_alive = alive
        self.observer.notify_observers()

    """ Sets the pet's poop level. """
    def set_poop(self, poop: int):
        self.poop = poop
        self.observer.notify_observers()

    """ Sets the pet's action. """
    def set_action(self, action, secondary_action=None):
        self.action = action
        self.secondary_action = secondary_action
        self.observer.notify_observers()

    """ Sets the pet's background. """
    def set_background(self, background: int):
        self.background = background
        self.observer.notify_observers()

    """ Sets the pet's weight. """
    def set_weight(self, weight: int):
        self.weight = weight
        self.observer.notify_observers()

    """ Sets the pet's poop level. """
    def set_poop_level(self, poop_level: int):
        self.poop_level = poop_level
        self.observer.notify_observers()

    """ Sets whether the pet's poop is visible. """
    def set_poop_visible(self, visible: bool):
        self.poop_visible = visible
        self.observer.notify_observers()

    """ Checks if the poop animation should be triggered. """
    def should_trigger_poop_animation(self):
        if self.poop_level >= 75:
            self.poop_visible = True  # Set poop as visible
            # Poop affects health negatively
            self.health = max(0, self.health - 3)
            return True
        return False

    """ Sets the pet's mood based on health level. """
    def set_mood(self):
        if not self.is_alive:
            self.mood = self.MOOD_DEAD
            self.action = "dead"
        elif 75 <= self.health <= 100:
            self.mood = self.MOOD_HAPPY
            self.action = "happy"
        elif 50 <= self.health < 75:
            self.mood = self.MOOD_MIDDLE
            self.action = "middle"
        elif 25 <= self.health < 50:
            self.mood = self.MOOD_ANGRY
            self.action = "angry"
        else:
            self.mood = self.MOOD_SAD
            self.action = "sad"

    """ Called by controller on an interval to update stats. """
    def update_stats(self):
        if not self.is_running or not self.is_alive or self.is_updating:
            return

        self.is_updating = True  # Acquire lock

        #Increament poop level and age
        self.poop_level = min(100, self.poop_level + 5)
        self.age += 1
        
        #Calc random decrease
        base_decrease = random.randint(1, 2)
        if self.weight > 325:
            # Overweight pets lose health faster
            self.health = max(0, self.health - base_decrease)
            self.weight = max(0, self.weight - (base_decrease // 2))
        elif self.age > 50:
            # Older pets lose health faster
            self.health = max(0, self.health - base_decrease)
            self.weight = max(0, self.weight - (base_decrease // 3))
        else:
            #Normal decrease
            self.health = max(0, self.health - (base_decrease // 2))
            self.weight = max(0, self.weight - (base_decrease // 4))

        # Decrease health if poop is visible
        if self.poop_visible:
            self.health = max(0, self.health - 3)

        # Check if pet is still alive
        if self.health <= 0 or self.weight <= 0:
            self.is_alive = False

        # Update mood based on current state
        self.set_mood()

        #Save and notify observers
        self.save_game_state()
        self.observer.notify_observers()
        
        self.is_updating = False  # Release lock

    """ Returns the pet's weight. """
    def get_weight(self) -> int:
        return self.weight

    """ Returns the pet's health. """
    def get_health(self) -> int:
        return self.health

    """ Returns the pet's poop level. """
    def get_poop_level(self) -> int:
        return self.poop_level

""" Manages saving and loading game data. """
class DataManager:

    """ Initializes the data manager. """
    def __init__(self):
        self.save_file = "save_file.json"
        self.default_data = {
            "name": "Sekitoritchi",
            "age": 1,
            "weight": 250,
            "mood": 0,
            "health": 100,
            "poop_level": 0,
            "is_alive": True,
            "poop_visible": False,
            "action": "happy",
            "background": 0
        }

    """ Saves the game data to a JSON file. """
    def save_data(self, data):
        try:
            with open(self.save_file, 'w') as f:
                #Converts/saves python object to JSON string
                json.dump(data, f, indent=4)
            return True
        except (IOError, json.JSONDecodeError) as e:
            print(f"Failed to save game data: {e}")
            return False

    """ Loads the game data from a JSON file. """
    def load_data(self):
        try:
            if os.path.exists(self.save_file): #Check if file exists
                with open(self.save_file, 'r') as f:
                    #Converts/loads JSON string to python object
                    return json.load(f)
            return self.default_data
        except (IOError, json.JSONDecodeError) as e:
            print(f"Failed to load game data: {e}")
            return self.default_data 

    """ Resets the game data. """
    def reset_data(self):
        self.save_data(self.default_data)

class Observer:
    """Manages observer callbacks and notifications."""
    def __init__(self):
        self._observers = []
        self.is_running = True

    """Add an observer callback function"""
    def add_observer(self, callback):
        if callback not in self._observers:
            self._observers.append(callback)

    """Remove an observer callback function"""
    def remove_observer(self, callback):
        if callback in self._observers:
            self._observers.remove(callback)

    """Notify all observers of a change"""
    def notify_observers(self):
        if not self.is_running:
            return
        for observer in self._observers:
            try:
                observer()
            except tk.TclError:
                # If we get a TclError, the window was probably destroyed
                self.is_running = False
                break

    """Stop the observer and cleanup"""
    def stop(self):
        self.is_running = False