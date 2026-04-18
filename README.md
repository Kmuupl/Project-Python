# Text RPG Dice Game
## Description
A console-based turn-based RPG written in Python.
The player explores dungeons, fights enemies using a dice-based combat system,
collects loot and faces a final boss.

## Features
- Grid-based dungeon exploration (WASD movement, no Enter needed)
- Fog of war — only visited areas are revealed
- Turn-based dice combat with critical hits
- Items: Health Potions and Stars of Luck
- Star mechanic: increases crit chance via weighted random
- Boss fight with inverted armor rules
- Save / load system
- Score saving to JSON
- Multiple difficulty levels

## Game Mechanics
### Normal enemies:
- Roll dice (1–6)
- Higher values are better
- Critical hit on **6** (20 damage)

### Boss fight:
- Rules are inverted
- Lower values are better
- Critical hit on **1**
- Player must adapt strategy

### Items
- **Health Potion** — restores 20 HP, capped at max HP
- **Star of Luck** — use before attack to increase crit chance by 10%

## How to run
1. Clone the repository:
git clone <your-repo-link>
cd Project-Python
2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  (Windows)
source .venv/bin/activate  (Linux/Mac)
3. Install dependencies
pip install -r requirements.txt
4. Run the game:
python main.py
5. Run tests
pytest tests/test_game.py -v

## Requirements
Python 3.10+
pytest
pytest-cov(for tests)