class Game:
    def __init__(self, player):
        self.player = playerself.locations = [
            0("Dungeon",  "Dark and cold...", "dungeon enemy"),
            1("Sewers",   "It smells...",     "sewers enemy"),
            2("Slums",    "Ruins everywhere", "slums enemy"),
            3("Castle",   "Cold stone walls", "castle enemy"),
            4("Throne",   "The final room",   "BOSS"), 
        ]
    def next_location(self):
