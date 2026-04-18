import random

class Dice:
    """Dice bag with standard and weighted roll support."""

    def __init__(self, count: int):
        self.count = count

    def roll(self) -> list[int]:
        """Roll all dice and return list of results."""

        return [random.randint(1, 6) for _ in range(self.count)]
    
    def roll_dice(self, crit_target: int | None = None, star_bonus: float = 0.0) -> int:
        """Roll a single die with optional bias toward crit_target.

        Args:
            crit_target: value to bias toward (6 for normal mode, 1 for boss mode)
            star_bonus: extra weight added to crit_target probability (0.0 = no bias)
        """

        if crit_target is None or star_bonus == 0.0:
            return random.randint(1, 6)
        weights = [1.0] * 6
        weights[crit_target - 1] += star_bonus * 6
        return random.choices([1, 2, 3, 4, 5, 6], weights=weights)[0]
    
    def __str__(self):
        """Return readable dice bag summary."""
        return f"Dices in bag: {self.count}"