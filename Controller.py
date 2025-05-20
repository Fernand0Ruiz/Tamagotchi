from Model import Model
import random
import time
import tkinter as tk

class Controller: 

    def __init__(self, tamagotchi, main_window):
        self.pet = tamagotchi
        self.main_window = main_window
        self.is_animating = False
        self.background_index = self.pet.get_background()
        self.update_interval = 15  # Update stats every 15 seconds
        self.next_update_time = time.time() + self.update_interval
        # Start the update timer
        self.schedule_next_update()

    """Call this function to save the game state"""
    def save_game(self):
        self.pet.save_game_state()

    """Call this function to load the game state"""
    def load_game(self):
        self.pet.load_game_state()

    """Call this function to reset the game"""
    def reset_game(self):
        self.pet.reset_game()
        #Reset the animation state
        self.is_animating = False

    """Schedule the next stats update"""
    def schedule_next_update(self):
        if not self.pet.is_running or not self.pet.is_alive:
            return
        try:
            # Calculate time until next update
            current_time = time.time()
            time_until_update = max(0, self.next_update_time - current_time)
            
            # Schedule the update
            self.update_timer = self.main_window.after(int(time_until_update * 1000), self.handle_update)
        except tk.TclError:
            self.pet.is_running = False

    """
        Handles the stats update.
    """
    def handle_update(self):
        print("handle_update called")  # Debug print
        if not self.is_animating and self.pet.is_running and self.pet.is_alive:
            print("Conditions met for update")  # Debug print
            self.pet.update_stats()
            # Check if we need to show poop animation
            if self.pet.should_trigger_poop_animation():
                print("Should trigger poop animation!")  # Debug print
                self.make_poop()
            # Schedule next update
            self.next_update_time = time.time() + self.update_interval
            self.schedule_next_update()

    """
        Plays an animation for a specified duration then returns to idle.
        Optional secondary action to composite alongside the main action (eating and pooping)..
    """
    def play_animation_sequence(self, action, duration=2, secondary_action=None):
        if not self.is_animating:
            #Set to true to prevent animation interuption
            self.is_animating = True

            # Set the action with optional secondary action
            self.pet.set_action(action, secondary_action)
            
            # Schedule return to idle
            self.main_window.after(int(duration * 1000), self.return_to_idle)
            return True
        return False

    """
        Returns the pets to it's idle state after being interacted with. 
    """ 
    def return_to_idle(self):
        self.pet.set_action(self.pet.get_action_mood())
        self.pet.set_background(self.background_index)

        #Set to false to allow animations again
        self.is_animating = False
        self.save_game()

        #Check if we need to update stats, b/c of interupted animation
        if time.time() >= self.next_update_time:
            self.handle_update()

    """
        Feed action button, increases weight and health and decreases poop level.
        Randomly selects to eat oniguri or dessert.
        Increment and decrement of stats is random (1-3).
    """
    def feed(self):
        if not self.is_animating and not self.pet.is_updating:
            increase = self.get_random_number(1, 3)
            self.pet.set_weight(self.pet.get_weight() + increase)
            self.pet.set_health(self.pet.get_health() + increase)
            self.pet.set_poop_level(self.pet.get_poop_level() + increase)
            choice = random.choice(["oniguri", "dessert"])
            self.play_animation_sequence("eat", 3, choice)
    
    """
        Dance action button, increases health and decreases poop level.
        Randomly selects to dance in left or right direction.
        Increment and decrement of stats is random (1-3).
    """
    def dance(self):
        if not self.is_animating and not self.pet.is_updating:
            increase = self.get_random_number(1, 3)

            self.pet.set_health(self.pet.get_health() + increase)
            self.pet.set_poop_level(self.pet.get_poop_level() - increase)
            choice = random.choice(["dance", "dance_reverse"])
            self.play_animation_sequence(choice, 3)

    """
        Sleep action button, decreases weight and increases health and poop level.
        Changes background to night-time background during sleep animation, 
        based on pet's current background. Increment and decrement of stats is random (1-3).
    """
    def sleep(self):
        if not self.is_animating and not self.pet.is_updating:
            increase = self.get_random_number(1, 3)
            self.pet.set_weight(self.pet.get_weight() - increase)
            self.pet.set_health(self.pet.get_health() + increase)
            self.pet.set_poop_level(self.pet.get_poop_level() + increase)
            #Determine's pet's current background and sets the night bg accordingly
            if(self.background_index in [5, 6, 7]):
                self.pet.set_background(7) #outside night bg index
            else:
                self.pet.set_background(4) #inside night bg index
            self.play_animation_sequence("sleep", 3)

    """
        Dice roll action button, selects a random animation reaction (postive or negative)
        with an asscosiated stat effect and a background change. Purpose is to stimulate
        a pet's reaction to a scenary change. 
    """
    def random_event(self):
        if not self.is_animating and not self.pet.is_updating:
            #Dice roll possible outcomes
            roll = {"fustrated":-5, "attention":-3, "look":3, "dance_reverse":5}
            #Change background to the next background index
            new_background = self.background_index + 1
            if(new_background > 7):
                new_background = 0 #reset to first background index
            self.background_index = new_background
            self.pet.set_background(new_background)

            #Rolls dice and applies stat effect and duration
            result = random.choice(list(roll.items()))
            self.pet.set_health(self.pet.get_health() + result[1])
            duration = 5 if result[0] == "fustrated" else 3
            self.play_animation_sequence(result[0], duration)

    def make_poop(self):
        if not self.is_animating and not self.pet.is_updating:
            self.play_animation_sequence("pooping", 2, "poop")
            self.pet.set_poop(True)
            self.pet.set_poop_visible(True)
            self.pet.set_poop_level(0)
            self.save_game()
        else:
            if self.pet.is_updating:
                self.main_window.after(100, self.make_poop)

    """
        Cleans up poop by resting poop stats to 0, for the next poop event.
    """
    def clean_poop(self):
        if self.pet.get_poop_visible():
            self.pet.set_poop(False)
            self.pet.set_poop_visible(False)
            self.pet.set_poop_level(0)
            self.save_game()
            return True
        return False

    """
    Returns a dictionary of the pet's stats. Instead of using getters and setters,
    this is a more convinient way for mass updates.
    """
    def get_pet(self):
        stats = {}    
        stats["name"] = self.pet.get_name()
        stats["age"] = self.pet.get_age()
        stats["weight"] = self.pet.get_weight()
        stats["mood"] = self.pet.get_mood()
        stats["health"] = self.pet.get_health()
        stats["poop"] = self.pet.get_poop()
        stats["poop_level"] = self.pet.get_poop_level()
        stats["is_alive"] = self.pet.get_is_alive()
        stats["action"] = self.pet.get_action()
        stats["background"] = self.pet.get_background()
        
        return stats
    
    def get_random_number(self, min, max):
        return random.randint(min, max)