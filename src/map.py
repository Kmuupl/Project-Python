from src.utils import slow_print

# Map tile meanings:
# "." - empty walkable tile
# "S" - start position
# "B" - boss room (ends exploration)
# "#" - wall (cannot enter)

TILE_DESCRIPTION: dict[str, str] = {
    "S": "You are at the entrance.",
    "B": "A dark presence fills the room",
    ".": "",
    "#": "",
}

class Map:
    """2D grid-based map with player movement via WASD."""
    PLAYER = "P"
    DEFAULT_GRID = [
        ["S", ".", ".", "#", "."],
        [".", "#", ".", "#", "."],
        [".", ".", ".", ".", "."],
        ["#", "#", ".", "#", "."],
        [".", ".", ".", ".", "B"],
    ]

    DIRECTION = {
        "w": (0, -1),
        "s": (0, 1),
        "a": (-1, 0),
        "d": (1, 0),
    }

    def __init__(self, grid: list[list[str]] | None = None):
        self.grid = self.DEFAULT_GRID if grid is None else grid 
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def render(self, player_x: int, player_y: int) -> None:
        """Print the map to console. Player shown as 'P'."""
        for row_idx, row in enumerate(self.grid):
            line = "  "
            for col_idx, title in enumerate(row):
                if col_idx == player_x and row_idx == player_y:
                    line += f"[{self.PLAYER}]"
                else:
                    line += f"[{tile}]"
            print(line)
        print()

    def move(self, x: int, y: int, direction: str) -> tuple[int, int]:
        if direction not in self.DIRECTION:
            return x, y
        dx, dy = self.DIRECTION[direction]
        new_x = x + dx
        new_y = y + dy
        if not (0 <= new_x < self.cols and 0 <= new_y < self.rows):
            slow_print("You can't go there — it's the edge of the world.")
            return x, y
        return new_x, new_y
    
    def get_tile(self, x: int, y: int) -> str:
        return self.grid[y][x]