import random

class Dice:
    """Dice bag with standard and weighted roll support."""
    def __init__(self, count: int):
        self.count = count

    def roll(self) -> list[int]:
        return [random.randint(1, 6) for _ in range(self.count)]
    
    def roll_dice(self, crit_target: int | None = None, star_bonus: float = 0.0) -> int:
        if crit_target is None or star_bonus == 0.0:
            return random.randint(1, 6)
        weights = [1.0] * 6
        weights[crit_target - 1] += star_bonus * 6
        return random.choices([1, 2, 3, 4, 5, 6], weights=weights)[0]
    
    def __str__(self):
        return f"Dices in bag: {self.count}"