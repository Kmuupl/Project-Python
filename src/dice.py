import random

class Dice:
    def __init__(self, count: int):
        self.count = count
    def roll(self) -> list[int]:
        return[random.randint(1, 6) for _ in range(self.count)]
    def __str__(self):
        return f"dices in inventory: {self.count}"