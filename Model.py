import json
import os

class Model:
    def __init__(self):
        self.data_manager = DataManager()
        self.load_game_state()
    
    def load_game_state(self):
        """Load the game state from saved data"""
        data = self.data_manager.load_data()
        self.name = data["name"]
        self.age = data["age"]
        self.weight = data["weight"]
        self.mood = data["mood"]
        self.health = data["health"]

    def save_game_state(self):
        """Save the current game state"""
        data = {
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "mood": self.mood,
            "health": self.health,
            "last_saved": None  # You could add timestamp here if you want
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
    
    def set_name(self,name: str):
        self.name = name

    def set_hunger(self,hunger: int):
        self.hunger = hunger
    
    def set_happiness(self, happiness: int):
        self.happiness = happiness

    def set_age(self, age: int):
        self.age = age

    def set_health(self, health: int):
        self.health = health

    def set_is_alive(self,alive: bool):
        self.alive = alive

    def set_poop(self, poop: int):
        self.poop = poop

class DataManager:
    def __init__(self):
        self.save_file = "tamagotchi_save.json"
        self.default_data = {
            "name": "Sekitoritchi",
            "age": 1,
            "weight": 250,
            "mood": 2,
            "health": 100,
            "last_saved": None
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