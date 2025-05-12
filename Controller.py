from Model import Model
import random
import time

class Controller: 

    def __init__(self, tamagotchi, main_window):
        self.pet = tamagotchi
        self.main_window = main_window
        self.is_animating = False
        self.background_index = self.pet.get_background()

    def save_game(self):
        self.pet.save_game_state()


    def load_game(self):
        self.pet.load_game_state()


    def play_animation_sequence(self, action, duration=2):
        """
        Play an animation for a specified duration then return to idle.
        
        Args:
            action: The action to play
            duration: How long to play the action in seconds
        """
        if not self.is_animating:
            self.is_animating = True
            # Set the action
            self.pet.set_action(action)
            # Schedule return to idle
            self.main_window.after(int(duration * 1000), self.return_to_idle)
            return True
        return False

    def return_to_idle(self):
        """Return the pet to idle animation"""
        self.pet.set_action("idle")
        self.pet.set_background(self.background_index)
        self.is_animating = False
        self.save_game()

    def feed(self):
        if not self.is_animating:
            self.pet.set_health(self.pet.get_health() + 15)
            self.pet.set_poop(self.pet.get_poop() + 15)
            self.play_animation_sequence("eat", 6)
    
    def dance(self):
        if not self.is_animating:
            self.pet.set_health(self.pet.get_health() + 15)
            self.pet.set_poop(self.pet.get_poop() + 15)
            self.play_animation_sequence("dance", 6)


    def sleep(self):
        if not self.is_animating:
            self.pet.set_health(self.pet.get_health() + 15)
            self.pet.set_poop(self.pet.get_poop() + 15)
            self.pet.set_background(4)
            self.play_animation_sequence("sleep", 6)


    def random_event(self):
        if not self.is_animating:
            new_background = self.background_index + 1
            if(new_background > 4):
                new_background = 0
            self.background_index = new_background
            self.pet.set_background(new_background)
            self.play_animation_sequence("poop", 6)
            self.save_game()
        
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
        stats["action"] = self.pet.get_action()
        stats["background"] = self.pet.get_background()
        
        return stats