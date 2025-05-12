import json
import os

class Model:
    def __init__(self):
        self.data_manager = DataManager()
        self._observers = []  # List to store observer callbacks
        self.load_game_state()
    
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
        for observer in self._observers:
            observer()
    
    def load_game_state(self):
        """Load the game state from saved data"""
        data = self.data_manager.load_data()
        self.name = data["name"]
        self.age = data["age"]
        self.weight = data["weight"]
        self.mood = data["mood"]
        self.health = data["health"]
        self.poop = data["poop"]
        self.alive = data["alive"]
        self.last_saved = data["last_saved"]
        self.action = data["action"]
        self.background = data["background"]

    def save_game_state(self):
        """Save the current game state"""
        data = {
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "mood": self.mood,
            "health": self.health,
            "poop": self.poop,
            "alive": self.alive,
            "last_saved": None,  # You could add timestamp here if you want
            "action": self.action,
            "background": self.background
        }
        return self.data_manager.save_data(data)

    def get_name(self) -> str:
        return self.name
    
    def get_hunger(self) -> int:
        return self.hunger 
    
    def get_happiness(self) -> int:
        return self.happiness
    
    def get_age(self) -> int:
        return self.age
    
    def get_health(self) -> int:
        return self.health
    
    def get_is_alive(self) -> bool:
        return self.alive
    
    def get_poop(self) -> int:
        return self.poop 

    def get_weight(self) -> int:
        return self.weight
    
    def get_mood(self) -> int:
        return self.mood
    
    def get_last_saved(self) -> str:
        return self.last_saved
    
    def get_action(self) -> str:
        return self.action 

    def get_background(self) -> str:
        return self.background
    
    def set_name(self,name: str):
        self.name = name
        self._notify_observers()

    def set_hunger(self,hunger: int):
        self.hunger = hunger
        self._notify_observers()
    
    def set_happiness(self, happiness: int):
        self.happiness = happiness
        self._notify_observers()

    def set_age(self, age: int):
        self.age = age
        self._notify_observers()

    def set_health(self, health: int):
        self.health = health
        self._notify_observers()

    def set_is_alive(self,alive: bool):
        self.alive = alive
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

class DataManager:
    def __init__(self):
        self.save_file = "tamagotchi_save.json"
        self.default_data = {
            "name": "Sekitoritchi",
            "age": 1,
            "weight": 250,
            "mood": 2,
            "health": 100,
            "poop": 0,  
            "alive": True,
            "last_saved": None,
            "action": "idle",
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