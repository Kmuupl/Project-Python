import time
import random
import json
from pathlib import Path
from src.dice import Dice
from src.item import StarOfLuck
from src.utils import slow_print, press_enter, safe_input

BASE_DAMAGE = 10
CRIT_DAMAGE = 20

class Player:
    def __init__(self, name: str, difficulty: int):
        self.inventory = []
        self.dice = Dice(50)
        self.name = name
        self.difficulty = difficulty
        self.boss_mode = False
        if difficulty == 0:
            self.hp = 100
        elif difficulty == 1:
            self.hp = 50
        elif difficulty == 2:
            self.hp = 20
        self.max_hp = self.hp
        self.stars: int = 0
        self.star_bonus_active: bool = False

    def __str__(self):
        return f"{self.name} | HP: {self.hp} | Difficulty: {self.difficulty} | Dice count: {self.dice.count}"
    
    def show_stats(self, enemy) -> None:
        slow_print(f"Your HP: {self.hp}")
        slow_print(f"Enemy name: {enemy.name} HP: {enemy.hp} Armor: {enemy.armor}")
        if enemy.reverse_armor:
            slow_print(f"This enemy has reverse armor! You need to roll less than or equal to {enemy.armor} to hit.")
        else:
            slow_print(f"Roll greater than or equal to {enemy.armor} to hit.")

        if self.boss_mode:
            slow_print("Rolling a 1 will result in a critical hit now.")
        else:
            slow_print("Rolling a 6 will result in a critical hit.")

    def take_turn(self, enemy) -> None:
        slow_print(f"Your turn, {self.name}")
        self.show_stats(enemy)
        while True:
            slow_print("Choose an action:")
            time.sleep(0.5)
            slow_print("[1] - Roll dice to attack")
            slow_print("[2] - Skip turn")
            slow_print("[3] - Info")
            slow_print("[4] - Inventory")
            choice = safe_input("Your choice: ", ["1", "2", "3", "4"])
            if choice == "1":
                time.sleep(0.5)
                self.roll_attack(enemy)
                break
            elif choice == "2":
                time.sleep(0.5)
                slow_print("..You take a deep breath and wait. Why not?..")
            elif choice == "3":
                time.sleep(0.5)
                self.show_stats(enemy)
            elif choice == "4":
                time.sleep(0.5)
                self._use_item_menu()

    def _use_item_menu(self) -> None:
        if not self.inventory:
            slow_print("Yout inventory is empty :( . )")
            return
        slow_print("Inventory:")
        for i, item in enumerate(self.inventory):
            slow_print(f" [{i}] {item}")
        slow_print(" [c] Cancel")
        valid = [str(i) for i in range(len(self.inventory))] + ["c"]
        choice = safe_input("Choose item: ", valid)
        if choice == "c":
            return
        item = self.inventory.pop(int(choice))
        item.use(self)

    def roll_attack(self, enemy) -> None:
        slow_print("..You are feeling a souls of your dice..")
        time.sleep(0.5)
        press_enter()
        crit_target = 1 if self.boss_mode else 6
        bonus = StarOfLuck.BONUS if self.star_bonus_active else 0.0
        self.star_bonus_active = False 
        roll = self.dice.roll_dice(crit_turget=crit_target, star_bonus=bonus)
        slow_print(f"You rolled: {roll}")
        time.sleep(0.5)
        is_crit = roll == crit_target

        if is_crit:
            if self.boss_mode:
                slow_print("Critical hit! The dice favor you with a perfect strike!")
            else:
                slow_print("Critical hit!!")

        damage = CRIT_DAMAGE if is_crit else BASE_DAMAGE

        if enemy.is_hit(roll):
            enemy.hp -= damage
            if is_crit:
                crit_msg = [
                    f"Your critical strike shatters {enemy.name}'s defenses, leaving it vulnerable.",
                    f"The dice align in your favor, delivering a devastating blow to {enemy.name}.",
                    f"With a surge of power, your critical hit sends {enemy.name} reeling.",
                    f"The critical strike pierces through {enemy.name}'s armor, causing massive damage.",
                    f"Your perfect roll unleashes a powerful attack, severely wounding {enemy.name}."
                ]
                slow_print(random.choice(crit_msg))
            else:
                dam_msg = [
                    f"The impact echoes through the chamber... {enemy.name} reels, barely holding its ground.",
                    f"Your strike lands with brutal precision — {enemy.name} lets out a distorted cry.",
                    f"The dice obey your will... the blow tears into {enemy.name}'s defenses.",
                    f"A solid hit. {enemy.name} stumbles, something inside it breaking.",
                    f"You push through the armor — {enemy.name} shudders under the force."
                ]
                slow_print(random.choice(dam_msg))
            slow_print(f"{enemy.name} HP: {enemy.hp}")
        else:
            miss_msg = [
                f"{enemy.name} anticipates your move, dodging with unnatural agility.",
                f"Your attack is deflected by {enemy.name}'s armor, leaving you off balance.",
                f"The dice betray you... {enemy.name} counters with a swift strike.",
                f"{enemy.name} laughs at your feeble attempt, shrugging off the attack.",
                f"Your blow glances off {enemy.name}'s defenses, leaving you vulnerable."
            ]
            slow_print(random.choice(miss_msg))

def choose_difficulty(name: str) -> int:
    slow_print(f"Okey, {name}. I remind you to choose difficulty.")
    time.sleep(0.5)
    slow_print("0 - Easy (MAX HP - 100)")
    slow_print("1 - Normal (50 HP)")
    slow_print("2 - Harder Normal (20 HP)")
    return int(safe_input("Your choice (0/1/2): ", ["0", "1", "2"]))

