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

    def save_game(self):
        self.pet.save_game_state()


    def load_game(self):
        self.pet.load_game_state()

    def reset_game(self):
        self.pet.reset_game()
        self.is_animating = False  # Reset animation state when game resets

    def schedule_next_update(self):
        """Schedule the next stats update"""
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

    def handle_update(self):
        """Handle the stats update"""
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

    def play_animation_sequence(self, action, duration=2, secondary_action=None):
        """
        Play an animation for a specified duration then return to idle.
        
        Args:
            action: The action to play
            duration: How long to play the action in seconds
            secondary_action: Optional secondary action to composite alongside the main action
        """
        if not self.is_animating:
            self.is_animating = True
            # Set the action with optional secondary action
            self.pet.set_action(action, secondary_action)
            
            # Schedule return to idle
            self.main_window.after(int(duration * 1000), self.return_to_idle)
            return True
        return False

    def return_to_idle(self):
        """Return the pet to idle animation"""
        # First clear the secondary action
        self.pet.set_action(self.pet.get_action(), None)
        # Then set the mood-based action
        self.pet.set_action(self.pet.get_action_mood())
        self.pet.set_background(self.background_index)
        self.is_animating = False
        self.save_game()
        # Check if we need to do an update now
        if time.time() >= self.next_update_time:
            self.handle_update()

    def feed(self):
        if not self.is_animating and not self.pet.is_updating:
            increase = self.get_random_number(1, 3)
            self.pet.set_weight(self.pet.get_weight() + increase)
            self.pet.set_health(self.pet.get_health() + increase)
            self.pet.set_poop_level(self.pet.get_poop_level() + increase)
            choice = random.choice(["oniguri", "dessert"])
            self.play_animation_sequence("eat", 6, choice)  # Add oniguri as secondary action
    
    def dance(self):
        if not self.is_animating and not self.pet.is_updating:
            increase = self.get_random_number(1, 3)
            self.pet.set_weight(self.pet.get_weight() - increase)
            self.pet.set_health(self.pet.get_health() + increase)
            self.pet.set_poop_level(self.pet.get_poop_level() - increase)
            choice = random.choice(["dance", "dance_reverse"])
            self.play_animation_sequence(choice, 6)


    def sleep(self):
        if not self.is_animating and not self.pet.is_updating:
            increase = self.get_random_number(1, 3)
            self.pet.set_weight(self.pet.get_weight() - increase)
            self.pet.set_health(self.pet.get_health() + increase)
            self.pet.set_poop_level(self.pet.get_poop_level() + increase)
            if(self.background_index in [5, 6, 7]):
                self.pet.set_background(7)  
            else:
                self.pet.set_background(4)
            self.play_animation_sequence("sleep", 6)

    def random_event(self):
        if not self.is_animating and not self.pet.is_updating:
            roll = {"fustrated":-5, "attention":-3, "look":3, "dance_reverse":5}
            new_background = self.background_index + 1
            if(new_background > 7):
                new_background = 0
            self.background_index = new_background
            self.pet.set_background(new_background)

            result = random.choice(list(roll.items()))
            self.pet.set_health(self.pet.get_health() + result[1])
            self.play_animation_sequence(result[0], 6)
            self.save_game()

    def make_poop(self):
        print("make_poop called")  # Debug print
        if not self.is_animating and not self.pet.is_updating:
            print("Starting poop animation")  # Debug print
            self.play_animation_sequence("pooping", 6, "poop")
            self.pet.set_poop(False)
            self.pet.set_poop_level(0)
            self.save_game()
        else:
            print("Cannot start poop animation - is_animating:", self.is_animating, "is_updating:", self.pet.is_updating)  # Debug print
            # Schedule the poop animation to start after the update is complete
            if self.pet.is_updating:
                print("Scheduling poop animation for after update")  # Debug print
                self.main_window.after(100, self.make_poop)  # Try again in 100ms

    def get_pet(self):
        stats = {}    
        # Remove the action setting that was causing recursion
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