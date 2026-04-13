from src.player import slow_print

class Enemy:
    def __init__(self, name: str):
        self.name = name
        self.reverse_armor = False
        self.damage = 2
        if name == "dungeon enemy":
            self.hp = 5
            self.armor = 1
        elif name == "sewers enemy":
            self.hp = 10
            self.armor = 2
        elif name == "slums enemy":
            self.hp = 20
            self.armor = 3
        elif name == "castle enemy":
            self.hp = 40
            self.armor = 4
        elif name == "BOSS":
            self.hp = 80
            self.armor = 5
            self.damage = 5
            self.reverse_armor = True

    def is_hit(self, roll: int) -> bool:
        if self.reverse_armor:
            return roll <= self.armor
        return roll >= self.armor
    
    def __str__(self):
        return f"{self.name} | HP: {self.hp} | Armor: {self.armor}"

    def attack(self, player) -> None:
        player.hp -= self.damage
        slow_print(f"{self.name} attacks! Your HP: {player.hp}")