import random
import json
import os

class Pet:
    def __init__(self, name):
        self.name = name
        self.energy = 5
        self.happiness = 5
        self.ores = 0
        self.log = []
        self.mood = "😊"
        self.last_feed_time = 0
        self.feed_cooldown = 3
        self.work_energy_cost = 2
        self.work_happiness_cost = 1
        self.work_ore_chance = 0.6
        self.work_cooldown = 0

    def get_mood(self):
        if self.happiness >= 4:
            return "😊"
        elif self.happiness >= 2:
            return "😐"
        else:
            return "😢"

    def get_status_bar(self, value, max_value=7):
        value = max(0, min(value, max_value))
        bar_length = 10
        filled = int((value / max_value) * bar_length)
        return "█" * filled + "░" * (bar_length - filled)

    def get_pet_art(self):
        if self.is_dead():
            return """
    ╔══════════════════════════════════╗
    ║           R.I.P.                 ║
    ║                                  ║
    ║    /\\___/\\                     ║
    ║   (  x x  )                      ║
    ║   (  =^=  )                      ║
    ║    (____)                        ║
    ╚══════════════════════════════════╝
            """
        elif self.energy >= 4 and self.happiness >= 4:
            return """
    ╔══════════════════════════════════╗
    ║           Happy Pet!             ║
    ║                                  ║
    ║    /\\___/\\                     ║
    ║   (  ^ω^  )                      ║
    ║   (  =^=  )                      ║
    ║    (____)                        ║
    ╚══════════════════════════════════╝
            """
        elif self.energy >= 4:
            return """
    ╔══════════════════════════════════╗
    ║           Energetic!             ║
    ║                                  ║
    ║    /\\___/\\                     ║
    ║   (  o o  )                      ║
    ║   (  =^=  )                      ║
    ║    (____)                        ║
    ╚══════════════════════════════════╝
            """
        elif self.energy >= 2:
            return """
    ╔══════════════════════════════════╗
    ║           Normal                 ║
    ║                                  ║
    ║    /\\___/\\                     ║
    ║   (  - -  )                      ║
    ║   (  =^=  )                      ║
    ║    (____)                        ║
    ╚══════════════════════════════════╝
            """
        else:
            return """
    ╔══════════════════════════════════╗
    ║           Tired...               ║
    ║                                  ║
    ║    /\\___/\\                     ║
    ║   (  x x  )                      ║
    ║   (  =^=  )                      ║
    ║    (____)                        ║
    ╚══════════════════════════════════╝
            """

    def get_action_art(self, action):
        if action == "feed":
            return """
    ╔══════════════════════════════════╗
    ║           Yummy!                 ║
    ║                                  ║
    ║    /\\___/\\                     ║
    ║   (  ^ω^  )                      ║
    ║   (  =^=  )  🍖                  ║
    ║    (____)                        ║
    ╚══════════════════════════════════╝
            """
        elif action == "play":
            return """
    ╔══════════════════════════════════╗
    ║           Play Time!             ║
    ║                                  ║
    ║    /\\___/\\                     ║
    ║   (  ^ω^  )                      ║
    ║   (  =^=  )  🎮                  ║
    ║    (____)                        ║
    ╚══════════════════════════════════╝
            """
        elif action == "work":
            return """
    ╔══════════════════════════════════╗
    ║           Working Hard!          ║
    ║                                  ║
    ║    /\\___/\\                     ║
    ║   (  -_-  )                      ║
    ║   (  =^=  )  ⛏️                  ║
    ║    (____)                        ║
    ╚══════════════════════════════════╝
            """
        elif action == "rest":
            return """
    ╔══════════════════════════════════╗
    ║           Zzz...                 ║
    ║                                  ║
    ║    /\\___/\\                     ║
    ║   (  - -  )                      ║
    ║   (  =^=  )  😴                  ║
    ║    (____)                        ║
    ╚══════════════════════════════════╝
            """
        elif action == "super_rest":
            return """
    ╔══════════════════════════════════╗
    ║           Super Rest!            ║
    ║                                  ║
    ║    /\\___/\\                     ║
    ║   (  ^ω^  )                      ║
    ║   (  =^=  )  ⭐                  ║
    ║    (____)                        ║
    ╚══════════════════════════════════╝
            """
        return ""

    def feed(self):
        if self.last_feed_time > 0:
            print(f"{self.name} is still digesting... Need to wait {self.last_feed_time} more turns.")
            self.log.append("Tried to feed, but still digesting.")
            return

        self.energy = min(7, self.energy + 2)
        print(self.get_action_art("feed"))
        print(f"{self.name} has been fed and feels energized!")
        self.log.append("Fed the pet.")
        
        self.last_feed_time = self.feed_cooldown

    def work(self):
        if self.happiness < 3:  # Cannot work when sad
            print(f"{self.name} is too sad to work. Play with them first!")
            self.log.append("Tried to work, but too sad.")
            return

        if self.energy < self.work_energy_cost:
            print(f"{self.name} is too tired to work.")
            self.log.append("Tried to work, but too tired.")
            return

        if self.work_cooldown > 0:
            print(f"{self.name} needs to rest before working again. Wait {self.work_cooldown} more turns.")
            self.log.append("Tried to work, but needs rest.")
            return

        # Consume energy and happiness
        self.energy = max(0, self.energy - self.work_energy_cost)
        self.happiness = max(0, self.happiness - self.work_happiness_cost)
        
        # Show work animation
        print(self.get_action_art("work"))
        
        # Chance to find ore
        if random.random() < self.work_ore_chance:
            self.ores += 1
            print(f"{self.name} found an ore while working!")
            self.log.append("Found an ore while working.")
        else:
            print(f"{self.name} worked hard but found nothing...")
            self.log.append("Worked but found nothing.")

        self.work_cooldown = 2  # Set work cooldown
        print(f"{self.name} is tired from working.")
        self.log.append("Pet worked.")

    def play(self):
        if self.energy < 1:
            print(f"{self.name} is too tired to play.")
            self.log.append("Tried to play, but too tired.")
            return

        if self.happiness >= 7:  # Already max happiness
            print(f"{self.name} is already very happy!")
            self.log.append("Tried to play, but already very happy.")
            return

        self.energy = max(0, self.energy - 1)
        self.happiness = min(7, self.happiness + 2)  # Increase happiness
        print(self.get_action_art("play"))
        print(f"{self.name} had a great time playing!")
        self.log.append("Played with the pet.")

    def rest(self):
        self.energy = min(7, self.energy + 3)
        print(self.get_action_art("rest"))
        print(f"{self.name} took a rest.")
        self.log.append("Pet rested.")

    def super_rest(self):
        if self.happiness < 3:  # Cannot use super rest when sad
            print(f"{self.name} is too sad to enjoy super rest. Play with them first!")
            self.log.append("Tried super rest, but too sad.")
            return

        if self.ores >= 2:
            self.energy = min(7, self.energy + 3)  # Restore energy
            self.happiness = min(7, self.happiness + 1)  # Increase happiness
            self.ores -= 2
            print(self.get_action_art("super_rest"))
            print(f"{self.name} had a SUPER REST!")
            self.log.append("Used super rest.")
        else:
            print("Not enough ores. Feed more to find them!")
            self.log.append("Tried super rest but lacked ores.")

    def tick(self):
        if self.is_dead():
            return

        # Suicide check - moved to front to ensure immediate handling
        if self.happiness <= 0:
            print(f"""
    ╔══════════════════════════════════╗
    ║           Suicide...             ║
    ║                                 ║
    ║    /\\___/\\                      ║
    ║   (  x x  )                     ║
    ║   (  =^=  )  💔                 ║
    ║    (____)                       ║
    ╚══════════════════════════════════╝
            """)
            print(f"{self.name} couldn't take it anymore and committed suicide...")
            self.log.append("Pet committed suicide due to extreme sadness.")
            return

        # Energy system
        if self.energy < 3:
            self.happiness = max(0, self.happiness - 1)
            print(f"{self.name} looks tired.")
            self.log.append("Energy is low.")
        
        if self.last_feed_time > 0:
            self.last_feed_time -= 1

        # Status check - only when not tired
        if self.happiness < 3 and self.energy >= 3:
            print(f"{self.name} seems sad...")
            self.log.append("Happiness is low.")

    def show_log(self):
        print("\n--- ACTION LOG ---")
        if not self.log:
            print("No actions yet.")
        else:
            for line in self.log[-10:]:  # Show last 10 logs
                print(f"- {line}")

    def is_dead(self):
        return self.happiness <= 0 or self.energy <= 0

    def __str__(self):
        return (f"\n{self.get_pet_art()}\n"
                f"{self.name} {self.get_mood()}\n"
                f"Energy:   [{self.get_status_bar(self.energy)}] {self.energy}/7\n"
                f"Happiness: [{self.get_status_bar(self.happiness)}] {self.happiness}/7\n"
                f"Ores: 💎 x {self.ores}")

    def save(self):
        data = {
            'name': self.name,
            'energy': self.energy,
            'happiness': self.happiness,
            'ores': self.ores,
            'log': self.log,
            'last_feed_time': self.last_feed_time,
            'work_energy_cost': self.work_energy_cost,
            'work_happiness_cost': self.work_happiness_cost,
            'work_ore_chance': self.work_ore_chance,
            'work_cooldown': self.work_cooldown
        }
        with open('pet_save.json', 'w') as f:
            json.dump(data, f)

    @classmethod
    def load(cls):
        if not os.path.exists('pet_save.json'):
            return None
        
        with open('pet_save.json', 'r') as f:
            data = json.load(f)
        
        pet = cls(data['name'])
        pet.energy = data['energy']
        pet.happiness = data['happiness']
        pet.ores = data['ores']
        pet.log = data['log']
        pet.last_feed_time = data['last_feed_time']
        pet.work_energy_cost = data['work_energy_cost']
        pet.work_happiness_cost = data['work_happiness_cost']
        pet.work_ore_chance = data['work_ore_chance']
        pet.work_cooldown = data['work_cooldown']
        return pet

    @staticmethod
    def delete_save():
        if os.path.exists('pet_save.json'):
            os.remove('pet_save.json')
