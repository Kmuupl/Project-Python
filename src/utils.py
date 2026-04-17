import time

def slow_print(text:str, delay: float = 0.03) -> None:
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def press_enter(msg: str = "Press Enter to continue...") -> None:
    input(msg)

def safe_input(prompt: str, valid_options: list) -> str:
    while True:
        choice = input(prompt).strip()
        if choice in valid_options:
            return choice
        slow_print("Sorry, nope. Please try again.")