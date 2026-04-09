class Player:
    def __init__(self, name: str, difficulty: int):
        self.inventory = []
        self.dice = Dice(count = 10)
        self.name = name
        if difficulty == 0:
            self.hp = 100
        elif difficulty == 1:
            self.hp = 50
        elif difficulty == 2:
            self.hp = 20
    def __str__(self):
        return f"{self.name} | HP: {self.hp} | Dices: {self.dice}"

def choose_difficulty() -> int:
    print(f"Okey, {name}. I remind you to choose difficulty.")
    print("0 - Easy (MAX HP)")
    print("1 - Normal (50 HP)")
    print("2 - Harder Normal (20 HP)")
    while True:
        choice = input("Your choice (0/1/2): ").strip()
        if coice in ("0", "1", "2"):
            return int(choice)
        print("Try Again :(")

name = input("Please, write yout name: ")
print(f"Hello, {name}!")

difficulty = choose_difficulty()
player = Player(name, difficulty)
print(player)

