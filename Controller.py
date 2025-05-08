from Model import Model

class Controller: 

    def __init__(self, tamagotchi):
        self.pet = tamagotchi


    def save_game(self):
        self.pet.save_game_state()


    def load_game(self):
        self.pet.load_game_state()


    def feed(self):
        self.pet.set_hunger(self.pet.get_hunger() - 15)
        self.pet.set_happiness(self.pet.get_happiness() + 15) 
        self.pet.set_health(self.pet.get_health() + 15)
        self.pet.set_poop(self.pet.get_poop() + 15)
        self.save_game()

    
    def dance(self):
        self.pet.set_happiness(self.pet.get_happiness() + 15)
        self.pet.set_hunger(self.pet.get_hunger() - 15)
        self.pet.set_health(self.pet.get_health() + 15)
        self.pet.set_poop(self.pet.get_poop() + 15)
        self.save_game()


    def sleep(self):
        self.pet.set_happiness(self.pet.get_happiness() + 15)
        self.pet.set_hunger(self.pet.get_hunger() - 15)
        self.pet.set_health(self.pet.get_health() + 15)
        self.pet.set_poop(self.pet.get_poop() + 15)
        self.save_game()


    def random_event(self):
        events = [self.dance, self.sleep, self.feed]
        random_event = random.choice(events)
        random_event()


    def get_pet(self):
        stats = {}    

        stats["name"] = self.pet.get_name()
        stats["age"] = self.pet.get_age()
        stats["weight"] = self.pet.get_weight()
        stats["mood"] = self.pet.get_mood()
        stats["health"] = self.pet.get_health()
        stats["poop"] = self.pet.get_poop()
        stats["is_alive"] = self.pet.get_is_alive()
        stats["last_saved"] = self.pet.get_last_saved()

        return stats