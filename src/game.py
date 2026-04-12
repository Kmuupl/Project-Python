import json
from pathlib import Path
from player import Player

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
        while self.current < len(self.locations):
            location, description, enemy_name = self.locations[self.current]
            print(f"You enter the {location}. {description}")
            enemy = Enemy(enemy_name)
            if not self.battle(enemy):
                break
            self.next_location()