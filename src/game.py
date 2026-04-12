class Game:
    def __init__(self, player):
        self.player = player
        self.locations = [
            ("Dungeon",  "Dark and cold...", "dungeon enemy"),
            ("Sewers",   "It smells...",     "sewers enemy"),
            ("Slums",    "Ruins everywhere", "slums enemy"),
            ("Castle",   "Cold stone walls", "castle enemy"),
            ("Throne",   "The final room",   "BOSS"), 
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