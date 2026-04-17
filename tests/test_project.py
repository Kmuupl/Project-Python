import pytest 
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.enemy import Enemy, Boss
from src.player import Player, BASE_DAMAGE, CRIT_DAMAGE
from src.dice import Dice

class TestEnemy:
    def test_dungeon_enemy_stats(self):
        e = Enemy("dungeon enemy")
        assert e.hp == 5
        assert e.armor == 1
        assert e.damage == 2
    
    def test_sewers_enemy_stats(self):
        e = Enemy("sewers enemy")
        assert e.hp == 10
        assert e.armor == 2
    
    def test_slums_enemy_stats(self):
        e = Enemy("slums enemy")
        assert e.hp == 20
        assert e.armor == 3

    def test_castle_enemy_stats(self):
        e = Enemy("castle enemy")
        assert e.hp == 40
        assert e.armor == 4

    def test_boss_stats(self):
        e = Boss()
        assert e.hp == 80
        assert e.armor == 5
        assert e.damage == 5

    def test_armor_hit(self):
        e = Enemy("dungeon enemy")
        assert e.is_hit(1) is True
        assert e.is_hit(2) is True
        assert e.is_hit(3) is True
        assert e.is_hit(4) is True
        assert e.is_hit(5) is True
        assert e.is_hit(6) is True

    def test_armor_miss(self):
        e = Enemy("castle enemy")
        assert e.is_hit(1) is False
        assert e.is_hit(2) is False
        assert e.is_hit(3) is False
    
    def test_reverse_armor_hit(self):
        e = Boss()
        assert e.is_hit(1) is True
        assert e.is_hit(2) is True
        assert e.is_hit(3) is True
        assert e.is_hit(4) is True
        assert e.is_hit(5) is True
        assert e.is_hit(6) is False

    def test_reverse_armor_miss(self):
        e = Boss()
        assert e.is_hit(6) is False

    def test_enemy_attack(self):
        player = Player("TestPlayer", 0)
        e = Enemy("dungeon enemy")
        e.attack(player)
        assert player.hp == 98

    def test_boss_attack(self):
        player = Player("TestPlayer", 0)
        e = Boss()
        e.attack(player)
        assert player.hp == 95

class TestPlayer:
    def test_easy_difficulty(self):
        p = Player("TestPlayer", 0)
        assert p.hp == 100
    
    def test_normal_difficulty(self):
        p = Player("TestPlayer", 1)
        assert p.hp == 50

    def test_harder_normal_difficulty(self):
        p = Player("TestPlayer", 2)
        assert p.hp == 20
    
    def test_boss_mode_default_false(self):
        p = Player("TestPlayer", 0)
        assert p.boss_mode is False

    def test_crit_value_normal_mode(self):
        p = Player("TestPlayer", 0)
        crit_value = 1 if p.boss_mode else 6
        assert crit_value == 6

    def test_crit_value_boss_mode(self):
        p = Player("TestPlayer", 0)
        p.boss_mode = True
        crit_value = 1 if p.boss_mode else 6
        assert crit_value == 1
class TestDice:
    def test_dice_roll_range(self):
        d = Dice(count = 50)
        for _ in range(100):
            roll = d.roll_dice()
            assert 1 <= roll <= 6

    def test_dice_roll_list(self):
        d = Dice(count = 5)
        result = d.roll()
        assert len(result) == 5

    def test_roll_value_range(self):
        d = Dice(count = 50)
        for val in d.roll():
            assert 1 <= val <= 6

class TestDamageValues:
    def test_base_damage(self):
        assert BASE_DAMAGE == 10

    def test_crit_damage(self):
        assert CRIT_DAMAGE == 20

    def test_crit_damage_greater_than_base(self):
        assert CRIT_DAMAGE > BASE_DAMAGE
        