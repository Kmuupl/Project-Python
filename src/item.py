from __future__ import annotations
from typing import TYPE_CHECKING
from src.utils import slow_print

if TYPE_CHECKING:
    from src.player import Player

class Item:
    """Base class for all collectible items."""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def use (self, player: Player) -> None:
        raise NotImplementedError(f"{self.name} not useble.")
    
    def on_pickup(self, player: Player) -> None:
        pass

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"
    
class HealthPotion(Item):
    """Restores 20 HP when used. Cannot exceed player's max HP."""
    HEAL_AMOUNT = 20

    def __init__(self):
        super().__init__("Health Potion", f"Restores {self.HEAL_AMOUNT} HP.")

    def use(self, player: Player) -> None:
        healed = min(self.HEAL_AMOUNT, player.max_hp - player.hp)
        player.hp += healed
        slow_print(f"You drink the potion and recover {healed} HP. HP: {player.hp}")

class StarOfLuck(Item):
    """Increases crit chance by 10% for one attack when used."""
    BONUS = 0.10   

    def __init__(self):
        super().__init__("Star of Luck", "Use before attack: +10% crit chance for one roll")

    def on_pickup(self, player: Player) -> None:
        player.stars += 1
        slow_print("You have a Star of Luck now!")

    def use(self, player) -> None:
        if player.stars <= 0:
            slow_print("No stars..")
            return
        player.stars -= 1
        player.star_bonus_active = True
        slow_print("The star glimmers.. You feel luckier!")