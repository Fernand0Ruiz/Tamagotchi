from Model import Model
import random
import time
import tkinter as tk

#Random value ranges for different actions
MIN = 3  # Minimum value for interactions (slightly better than base decrease)
MAX = 5  # Maximum value for interactions (significantly better but not overwhelming)

class Controller: 

    def __init__(self, main_window, observer):
        self.pet = Model(observer) # Initialize the model with the observer
        self.main_window = main_window # Store the main window
        self.is_animating = False # Track if the animation is playing
        self.background_index = self.pet.get_background() # Get the background index
        self.update_interval = 15  # Update stats every 15 seconds
        self.update_timer = None # Track the update timer
        # Start the update timer
        self.handle_update()

    """
        Cancels the update timer if it exists.
    """
    def _cancel_update_timer(self):
        if self.update_timer:
            self.main_window.after_cancel(self.update_timer)
            self.update_timer = None

    """
        Call this function to save the game state.
    """
    def save_game(self):
        self.pet.save_game_state()

    """
        Call this function to load the game state.
    """
    def load_game(self):
        self.pet.load_game_state()

    """
        Call this function to reset the game.
    """
    def reset_game(self):
        # Cancel any existing timer
        self._cancel_update_timer()
        self.pet.reset_game()
        #Reset the animation state
        self.is_animating = False
        # Restart the update cycle
        self.handle_update()

    """
        Handles the stats update and schedules the next update.
        Uses absolute time to prevent drift and ensures clean timer management.
    """
    def handle_update(self):
        # Cancel any existing timer to prevent multiple timers
        self._cancel_update_timer()

        # Only proceed if pet is running, alive, and not animating
        if self.pet.is_running and self.pet.is_alive and not self.is_animating:
            print("Stats updated!")
            self.pet.update_stats()

            #Check if pet needs to poop 
            if self.pet.should_trigger_poop_animation():
                self.make_poop()

        # Schedule next update using absolute time to prevent drift
        self.update_timer = self.main_window.after(self.update_interval * 1000, self.handle_update)

    """
        Stops the update cycle and clean up timers.
    """
    def stop(self):
        self._cancel_update_timer()
        self.pet.stop()

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

        # Force an update check since animation might have delayed it
        self.handle_update()

    """
        Feed action button, increases weight and health and decreases poop level.
        Randomly selects to eat oniguri or dessert.
        Increment and decrement of stats is random (1-3).
    """
    def feed(self):
        if not self.is_animating and not self.pet.is_updating:
            increase = random.randint(MIN, MAX)
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
            increase = random.randint(MIN, MAX)

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
            increase = random.randint(MIN, MAX)
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
            roll = {"fustrated":-MAX, "attention":-MIN, "look":MIN, "dance_reverse":MAX}
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

    """
        Plays the poop animation and sets the poop visible to true, until cleaned.
        Restores the poop level to 0, for next poop event.
    """
    def make_poop(self):
        if not self.is_animating and not self.pet.is_updating:
            print("Poop animation intiated.")
            self.play_animation_sequence("pooping", 2, "poop")
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
            print("Poop cleaned.")
            self.pet.set_poop_visible(False)
            self.save_game()
            return True
        return False

    """
        Returns a dictionary of the pet's stats.
    """
    def get_pet(self):
        return self.pet.get_pet()

    """
        Returns the secondary action of the pet.
    """
    def get_secondary_action(self) -> str:
        return self.pet.get_secondary_action()

    """
        Sets the name of the pet.
    """
    def set_name(self, name: str):
        self.pet.set_name(name)