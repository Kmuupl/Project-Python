import json
import time
from pathlib import Path
from datetime import date

from src.enemy import Enemy
from src.player import slow_print, press_enter

SAVE_FILE = Path("data/save.json")
SCORE_FILE = Path("data/scores.json")

class Game:
    def __init__(self, player):
        self.player = player
        data_path = Path("data/location.json")
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.locations = [
            (loc["name"], loc["description"], loc["enemy"]) for loc in data
        ]
        self.current = 0

    def next_location(self):
        if self.current < len(self.locations) - 1:
            self.current += 1

    def battle(self, enemy) -> bool:
        is_boss = enemy.name == "BOSS"
        if is_boss:
            slow_print("Something feels different..")
            time.sleep(1)
            slow_print("A terrifying presence fills the room..")
            time.sleep(1)
            slow_print("The BOSS appears! Prepare for the final battle!")
            slow_print("Its armor is.. oddly weak. But its strength is immense.")
            self.player.boss_mode = True
        else:
            slow_print(f"A {enemy.name} appears! Get ready to fight!")
        press_enter()

        while self.player.hp > 0 and enemy.hp > 0:
            self.player.take_turn(enemy)

            if enemy.hp <= 0:
                break

            slow_print(f"{enemy.name} prepares to attack...")
            time.sleep(1)
            slow_print(f"{enemy.name} watches your every move...")
            time.sleep(0.7)
            enemy.attack(self.player)
            press_enter()

        self.player.boss_mode = False

        if enemy.hp <= 0:
            slow_print(f"You defeated the {enemy.name}!")
            if is_boss:
                slow_print("With the BOSS defeated, a sense of relief washes over you.")
            press_enter("Continue your adventure...")
            return True
        if self.player.hp <= 0:
            slow_print("You have been defeated..")
            slow_print("The world fades to black as you fall..")
            return False
            
    def run(self):
        if SAVE_FILE.exists():
            choice = input("Load saved game? (y/n): ").strip().lower()
            if choice == "y":
                if self.load_game():
                    slow_print("Game loaded. Resuming...")
                else:
                    slow_print("Starting new game.")
        while self.current < len(self.locations):
            location, description, enemy_name = self.locations[self.current]
            slow_print(f"You enter the {location}.")
            slow_print(f"{description}")
            press_enter()

            enemy = Enemy(enemy_name)
            if not self.battle(enemy):
                self.save_score()
                slow_print("Game Over. Your bones will tell the tale.")
                return

            self.save_game()
            self.next_location()

        
        slow_print("Congratulations! You completed the game!")
        self.save_score()
        SAVE_FILE.unlink(missing_ok=True)

    def save_game(self) -> None:
        data = {
            "name": self.player.name,
            "difficulty": self.player.difficulty,
            "current_location": self.current,
            "date": str(date.today()),
            "hp": self.player.hp,
            "inventory": self.player.inventory,
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        slow_print("Game saved successfully.")

    def load_game(self) -> bool:
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.player.name = data["name"]
            self.player.hp = data["hp"]
            self.player.inventory = data["inventory"]
            self.current = data["current_location"]
            slow_print("Game loaded successfully.")
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            slow_print("No saved game found.")
            return False
        
    def save_score(self) -> None:
        location_name = self.locations[self.current][0]
        score_entry = {
            "name": self.player.name,
            "difficulty": self.player.difficulty,
            "location": location_name,
            "date": str(date.today()),
        }
        try:
            with open(SCORE_FILE, "r", encoding="utf-8") as f:
                scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []
        scores.append(score_entry)
        with open(SCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2, ensure_ascii=False)
        slow_print(f"Score saved successfully. Location: {location_name}")