import os
import time
import msvcrt
from src.utils import slow_print

TILE_SYMBOLS: dict[str, str] = {
    ".": "   ",
    "S": "   ",
    "B": " B ",
    "#": "███",
    "?": " ? ",
}

TILE_DESCRIPTION: dict[str, str] = {
    "S": "You are at the entrance.",
    "B": "A dark presence fills the room",
    ".": "",
    "#": "",
}

def clear_screen() -> None:
    print("\033[H\033[J", end="", flush=True)

def get_key() -> str:
    key = msvcrt.getch()
    if key in (b"\x00", b"\xe0"):
        msvcrt.getch()
        return ""
    return key.decode("utf-8", errors="ignore").lower()

class Map:
    """2D grid-based map with player movement via WASD."""
    PLAYER_SYMBOL = " P "
    FOG_SYMBOL = "///"
    DEFAULT_GRID: list[list[str]] = [
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
        ["#", "S", ".", ".", ".", "#", ".", ".", ".", ".", "#"],
        ["#", ".", "#", "#", ".", "#", ".", "#", "#", ".", "#"],
        ["#", ".", "#", ".", ".", ".", ".", ".", "#", ".", "#"],
        ["#", ".", ".", ".", "#", "#", "#", ".", ".", ".", "#"],
        ["#", "#", ".", "#", ".", ".", ".", "#", ".", "#", "#"],
        ["#", ".", ".", ".", ".", "#", ".", ".", ".", ".", "#"],
        ["#", ".", "#", "#", ".", ".", "#", "#", ".", ".", "#"],
        ["#", ".", ".", ".", ".", "#", ".", ".", ".", "B", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ]

    DIRECTIONS: dict[str, tuple[int, int]] = {
        "w": (0, -1),
        "s": (0, 1),
        "a": (-1, 0),
        "d": (1, 0),
    }

    def __init__(self, grid: list[list[str]] | None = None):
        self.grid = [row[:] for row in (grid if grid is not None else self.DEFAULT_GRID)]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.visited: set[tuple[int, int]] = set()

    def find_start(self) -> tuple[int, int]:
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile == "S":
                    return x, y
        return 1, 1

    def reveal(self, x: int, y: int, radius: int = 2) -> None:
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                nx, ny = x + dx, y+ dy
                if 0 <= nx < self.cols and 0 <= ny < self.rows:
                    self.visited.add((nx, ny))

    def render(self, player_x: int, player_y: int, player_hp: int, stars: int) -> None:
        clear_screen()

        width = self.cols * 3 + 2
        print("  |" + "=" * (width - 2) + "|  ")

        for row_idx, row in enumerate(self.grid):
            line = "  |"
            for col_idx, tile in enumerate(row):
                pos = (col_idx, row_idx)
                if col_idx == player_x and row_idx == player_y:
                    line += self.PLAYER_SYMBOL
                elif pos not in self.visited:
                    line += self.FOG_SYMBOL
                else:
                    line += TILE_SYMBOLS.get(tile, " ? ")
            line += "|"
            print(line)
        print("  |" + "=" * (width - 2) + "|  ")

        tile = self.get_tile(player_x, player_y)
        hint = TILE_DESCRIPTION.get(tile, "")
        hint_str = f"   [{hint}]" if hint else ""
        print(f"    HP: {player_hp}     Stars: {stars}{hint_str}")
        print("WASD to move Q to quite")

    def move(self, x: int, y: int, direction: str) -> tuple[int, int]:
        if direction not in self.DIRECTIONS:
            return x, y
        dx, dy = self.DIRECTIONS[direction]
        new_x, new_y = x + dx, y + dy
        if not (0 <= new_x < self.cols and 0 <= new_y < self.rows):
            return x, y
        if self.grid[new_y][new_x] == "#":
            return x, y
        return new_x, new_y
    
    def get_tile(self, x: int, y: int) -> str:
        return self.grid[y][x]