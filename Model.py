
class Tamagotchi:

    def __init__(self, name):
        self.name = name
        self.hunger = 0
        self.happiness = 0
        self.age = 0
        self.health = 100
        self.alive = True
        self.sick = False
    
    def __init__(self, name, hunger, happiness, age, health, alive, sick):
        self.name = name
        self.hunger = hunger
        self.happiness = happiness
        self.age = age
        self.health = health
        self.alive = alive
        self.sick = sick

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
    
    def get_is_sick(self) -> bool:
        return self.sick
    
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

    def set_is_sick(self, sick: bool):
        self.sick = sick
    