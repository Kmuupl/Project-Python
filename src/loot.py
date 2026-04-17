from __future__ import annotations
import random
from src.item import Item, HealthPotion, StarOfLuck

LOOT_TABLE: list[tuple[type[Item], float]] = [
    (HealthPotion, 0.5),
    (StarOfLuck, 0.3),
]

class LootTable:
    """Handles random item drops after battles. Game doesn't know what items exist."""
    def roll(self) -> list[Item]:
        dropped = []
        for item_class, chance in LOOT_TABLE:
            if random.random() < chance:
                dropped.append(item_class())
        return dropped