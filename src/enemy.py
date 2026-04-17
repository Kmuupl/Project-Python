from __future__ import annotations
from src.utils import slow_print

ENEMY_DATA = {
    "dungeon enemy": {"hp": 5, "armor": 1, "damage": 2},
    "sewers enemy": {"hp": 10, "armor": 2, "damage": 2},
    "slums enemy": {"hp": 20, "armor": 3, "damage": 2},
    "castle enemy": {"hp": 40, "armor": 4, "damage": 2},
    "BOSS": {"hp": 80, "armor": 5, "damage": 5}
}


class Enemy:
    """Base enemy class. Loads stats from ENEMY_DATA by name."""
    def __init__(self, name: str):
        if name not in ENEMY_DATA:
            raise ValueError(f"Unknown enemy type: {name}")
        stats = ENEMY_DATA[name]
        self.name = name
        self.hp = stats["hp"]
        self.armor = stats["armor"]
        self.damage = stats["damage"]

    def is_hit(self, roll: int) -> bool:
        """Returns True if roll meets or exceeds armor threshold."""
        return roll >= self.armor
    
    def attack(self, player) -> None:
        """Deal damage to player."""
        player.hp -= self.damage
        slow_print(f"{self.name} attacks! Your HP: {player.hp}")

    def __str__(self):
        return f"{self.name} | HP: {self.hp} | Armor: {self.armor}"
    
class Boss(Enemy):
    """Boss enemy with inverted armor mechanic — lower rolls hit harder."""
    NAME = "BOSS"

    def __init__(self):
        super().__init__(self.NAME)

    def is_hit(self, roll: int) -> bool:
        """Returns True if roll is less than or equal to armor."""
        return roll <= self.armor

    def __str__(self):
        return super().__str__() + " [BOSS]"