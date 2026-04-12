import json
from pathlib import Path
from datetime import date

SAVE_FILE = Path("data/save.json")
SCORE_FILE = Path("data/scores.json")

class Game:
    def __init__(self, player):
        self.player = player
        data_path = Path("data/locations.json")
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.locations = [
            (loc["name"], loc["description"], loc["enemy_name"]) for loc in data
        ]
        self.current = 0
    def next_location(self):
        if self.current < len(self.locations) - 1:
            self.current += 1
        return self.locations[self.current]
    def battle(self, enemy):
        print(f"You encounter a {enemy}!")
        while self.player.hp > 0 and enemy.hp > 0:
            self.player.attack(enemy)
            if enemy.hp > 0:
                enemy.attack(self.player)
            else:
                print(f"You defeated the {enemy}!")
        if self.player.hp <= 0:
            print("You have been defeated... Game Over.")
            return False
        return True
    def run(self):
        if SAVE_FILE.exists():
            choice = input("Load saved game? (y/n): ").strip().lower()
            if choice == "y":
                if self.load_game():
                    print("Game loaded. Resuming...")
                else:
                    print("Starting new game.")
        while self.current < len(self.locations):
            location, description, enemy_name = self.locations[self.current]
            print(f"You enter the {location}. {description}")
            enemy = Enemy(enemy_name)
            if not self.battle(enemy):
                self.save_score()
                break
            self.save_score()
            self.next_location()
        else:
            print("Congratulations! You completed the game!")
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
        print("Game saved successfully.")
    def load_game(self) -> bool:
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.player.name = data["name"]
            self.player.hp = data["hp"]
            self.player.inventory = data["inventory"]
            self.current = data["current_location"]
            print("Game loaded successfully.")
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            print("No saved game found.")
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
        print(f"Score saved successfully. Location: {location_name}")