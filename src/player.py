import time
import random
import json
from pathlib import Path
from src import enemy

def slow_print(text:str, delay: float = 0.03) -> None:
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def press_enter(msg: str = "Press Enter to continue...") -> None:
    input(msg)

class Player:
    def __init__(self, name: str, difficulty: int):
        self.inventory = []
        self.name = name
        if difficulty == 0:
            self.hp = 100
        elif difficulty == 1:
            self.hp = 50
        elif difficulty == 2:
            self.hp = 20
        self.difficulty = difficulty
        self.boss_mode = False

    def __str__(self):
        return f"{self.name} | HP: {self.hp}"
    
    def show_stats(self, enemy) -> None:
        slow_print(f"Your HP: {self.hp}")
        slow_print(f"Enemy name: {enemy.name} HP: {enemy.hp} Armor: {enemy.armor}")
        if enemy.reverse_armor:
            slow_print(f"This enemy has reverse armor! You need to roll less than or equal to {enemy.armor} to hit.")
        else:
            slow_print(f"Roll greater than or equal to {enemy.armor} to hit.")

    def take_turn(self, enemy) -> None:
        slow_print(f"Your turn to attack, {self.name}!")
        self.show_stats(enemy)
        while True:
            slow_print("Choose an action:")
            time.sleep(0.5)
            slow_print("[1] - Roll dice to attack")
            slow_print("[2] - Skip turn")
            slow_print("[3] - Info")
            choice = input("Your choice: ").strip()
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
            else:
                time.sleep(0.5)
                slow_print("Sorry, I didn't understand your choice.")

    def roll_attack(self, enemy) -> None:
        slow_print("..You are feeling a souls of your dice..")
        time.sleep(0.5)
        press_enter()
        roll = random.randint(1, 6)
        slow_print(f"You rolled: {roll}")
        time.sleep(0.5)

        if self.boss_mode:
            is_crit = roll == 1
            if is_crit:
                slow_print("Critical hit! The dice favor you with a perfect strike!")
        else:
            is_crit = roll == 6
            if is_crit:
                slow_print("Critical hit! The dice favor you with a perfect strike!")
        damage = 20 if is_crit else 10

        if enemy.is_hit(roll):
            enemy.hp -= damage
            if is_crit:
                crits = [
                    f"Your critical strike shatters {enemy.name}'s defenses, leaving it vulnerable.",
                    f"The dice align in your favor, delivering a devastating blow to {enemy.name}.",
                    f"With a surge of power, your critical hit sends {enemy.name} reeling.",
                    f"The critical strike pierces through {enemy.name}'s armor, causing massive damage.",
                    f"Your perfect roll unleashes a powerful attack, severely wounding {enemy.name}."
                ]
                slow_print(random.choice(crits))
            else:
                messages = [
                    f"The impact echoes through the chamber... {enemy.name} reels, barely holding its ground.",
                    f"Your strike lands with brutal precision — {enemy.name} lets out a distorted cry.",
                    f"The dice obey your will... the blow tears into {enemy.name}'s defenses.",
                    f"A solid hit. {enemy.name} stumbles, something inside it breaking.",
                    f"You push through the armor — {enemy.name} shudders under the force."
                ]
                slow_print(random.choice(messages))
            slow_print(f"{enemy.name} HP: {enemy.hp}")
        else:
            misses = [
                f"{enemy.name} anticipates your move, dodging with unnatural agility.",
                f"Your attack is deflected by {enemy.name}'s armor, leaving you off balance.",
                f"The dice betray you... {enemy.name} counters with a swift strike.",
                f"{enemy.name} laughs at your feeble attempt, shrugging off the attack.",
                f"Your blow glances off {enemy.name}'s defenses, leaving you vulnerable."
            ]
            slow_print(random.choice(misses))

def choose_difficulty(name: str) -> int:
    slow_print(f"Okey, {name}. I remind you to choose difficulty.")
    time.sleep(0.5)
    slow_print("0 - Easy (MAX HP)")
    slow_print("1 - Normal (50 HP)")
    slow_print("2 - Harder Normal (20 HP)")
    while True:
        choice = input("Your choice (0/1/2): ").strip()
        if choice in ("0", "1", "2"):
            return int(choice)
        slow_print("Try Again D:")


