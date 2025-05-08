from Model import Tamagotchi

class Controller: 
    def __init__(self):
        self.pet = Tamagotchi("Tamagotchi", 0, 0, 0, 100, True, False)

    def feed(self):
        self.pet.set_hunger(self.pet.get_hunger() - 15)
        self.pet.set_happiness(self.pet.get_happiness() + 15) 
        self.pet.set_health(self.pet.get_health() + 15)
        self.pet.set_poop(self.pet.get_poop() + 15)
        

