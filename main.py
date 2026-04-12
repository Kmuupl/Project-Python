from src.dice import Dice
from src.player import Player, choose_difficulty
from src.enemy import Enemy
from src.game import Game


def main():
    name = input("Please, write your name: ")
    print(f"Hello, {name}!")
    
    difficulty = choose_difficulty(name)
    player = Player(name, difficulty)
    print(player)

    game = Game(player)
    game.run()
if __name__ == "__main__":
    main()