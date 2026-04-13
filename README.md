# Text RPG Dice Game
## Description
This is a console-based text RPG game written in Python.
The player progresses through several locations, fighting enemies using a dice-based combat system.  
Each battle is turn-based and requires player interaction.

## Features
- Turn-based combat system
- Dice-based attack mechanics
- Critical hits (normal and inverted for boss)
- Unique boss fight with inverted rules
- Multiple locations loaded from JSON file
- Save / load system
- Score saving to JSON
- Atmospheric text output (delays, immersive messages)

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
pytest (for tests)