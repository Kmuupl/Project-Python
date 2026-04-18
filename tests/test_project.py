import pytest 
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.enemy import Enemy, Boss
from src.player import Player, BASE_DAMAGE, CRIT_DAMAGE
from src.dice import Dice
from src.item import HealthPotion, StarOfLuck
from src.location import Location
from src.loot import LootTable
from src.map import Map

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

    def test_unknown_enemy_raises(self):
        with pytest.raises(ValueError):
            Enemy("enemy")

    def test_armor_hit(self):
        e = Enemy("dungeon enemy")
        for roll in range(1, 6):
            assert e.is_hit(roll) is True

    def test_armor_miss(self):
        e = Enemy("castle enemy")
        assert e.is_hit(1) is False
        assert e.is_hit(2) is False
        assert e.is_hit(3) is False
    
    def test_reverse_armor_hit(self):
        e = Boss()
        for roll in range(1, 5):
            assert e.is_hit(roll) is True
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

    def test_max_hp_equals_starting_hp(self):
        p = Player("TestPlayer", 0)
        assert p.max_hp == 100
    
    def test_boss_mode_default_false(self):
        p = Player("TestPlayer", 0)
        assert p.boss_mode is False

    def test_stars_default_zero(self):
        p = Player("TestPlayer", 0)
        assert p.stars == 0

    def test_star_bonus_default_false(self):
        p = Player("TestPlayer", 0)
        assert p.star_bonus_active is False

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

    def test_biased_roll_range(self):
        d = Dice(count=50)
        for _ in range(100):
            roll = d.roll_dice(crit_target=6, star_bonus=0.5)
            assert 1 <= roll <= 6

    def test_no_bias_without_target(self):
        d = Dice(count=50)
        roll = d.roll_dice(crit_target=None, star_bonus=0.0)
        assert 1 <= roll <= 6

class TestDamageValues:
    def test_base_damage(self):
        assert BASE_DAMAGE == 10

    def test_crit_damage(self):
        assert CRIT_DAMAGE == 20

    def test_crit_damage_greater_than_base(self):
        assert CRIT_DAMAGE > BASE_DAMAGE
        
class TestItem:
    def test_health_potion_heals(self):
        p = Player("TestPlayer", 0)
        p.hp = 60
        potion = HealthPotion()
        potion.use(p)
        assert p.hp == 80

    def tets_health_potion_max(self):
        p = Player("TestPlayer", 0)
        p.hp = 95
        potion = HealthPotion()
        potion.use(p)
        assert p.hp == 100

    def test_star_pickup(self):
        p = Player("TestPlayer", 0)
        star = StarOfLuck()
        star.on_pickup(p)
        assert p.stars == 1

    def test_star_use(self):
        p = Player("TestPlayer", 0)
        p.stars = 1
        star = StarOfLuck()
        star.use(p)
        assert p.star_bonus_active is True
        assert p.stars == 0

    def test_star_use_without_stars(self):
        p = Player("TestPlayer", 0)
        star = StarOfLuck()
        star.use(p)
        assert p.star_bonus_active is False

class TestLocation:
    def test_location_fields(self):
        loc = Location("Dungeon", "Dark and cold", "dungeon enemy")
        assert loc.name == "Dungeon"
        assert loc.description == "Dark and cold"
        assert loc.enemy == "dungeon enemy"

    def test_location_is_dataclass(self):
        loc1 = Location("A", "B", "C")
        loc2 = Location("A", "B", "C")
        assert loc1 == loc2

class TestLootTable:
    def test_roll_returns_list(self):
        lt = LootTable()
        result = lt.roll()
        assert isinstance(result, list)

    def test_roll_items_are_valid(self):
        lt = LootTable()
        for _ in range(50):
            items = lt.roll()
            for item in items:
                assert hasattr(item, "use")
                assert hasattr(item, "name")

class TestMap:
    def test_find_start(self):
        m = Map()
        x, y = m.find_start()
        assert m.get_tile(x, y) == "S"

    def test_move_into_wall(self):
        m = Map()
        x, y = m.find_start()
        original = (x, y)
        new_x, new_y = m.move(x, y, "a")
        tile = m.get_tile(new_x, new_y)
        assert tile != "#"

    def test_move_boundary_does_not_crash(self):
        m = Map()
        new_x, new_y = m.move(1, 0, "w")
        assert new_y >= 0

    def test_reveal_adds_to_visited(self):
        m = Map()
        assert len(m.visited) == 0
        m.reveal(1, 1, radius=1)
        assert len(m.visited) > 0

    def test_get_tile_correct(self):
        m = Map()
        assert m.get_tile(0, 0) == "#"