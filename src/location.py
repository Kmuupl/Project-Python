from dataclasses import dataclass

@dataclass
class Location:
    """Represents a single game location with its name, description and enemy."""
    name: str
    description: str
    enemy: str