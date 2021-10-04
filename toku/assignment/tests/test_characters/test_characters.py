import math
import pytest
from attr import attributes
from fightclub_setup.superhero_api import *
from characters.characters import *
from tests.test_characters.conftest import good_character

attributes = [
    "intelligence",
    "strength",
    "speed",
    "durability",
    "power",
    "combat"
]

class TestCharacters:
    def test_build_character_success(self, random_id):
        character_data = get_character(random_id)
        character = build_character(character_data)
        assert character
        assert isinstance(character, Character)

    def test_build_character_fail(self):
        character_data = get_character(0)
        character = build_character(character_data)
        assert not isinstance(character, Character)
    
    def test_assign_stats_stamina_success(self, random_id):
        character_data = get_character(random_id)
        character = build_character(character_data)
        for attribute in attributes:
            assert hasattr(character, f"AS_{attribute}")

    def test_assign_stats_stamina_fail(self):
        character_data = get_character(0)
        character = build_character(character_data)
        for attribute in attributes:
            assert not hasattr(character, f"AS_{attribute}")

    def test_assign_global_stamina_success(self, random_id):
        character_data = get_character(random_id)
        character = build_character(character_data)
        assert hasattr(character, "actual_stamina")

    def test_assign_global_stamina_fail(self):
        character_data = get_character(0)
        character = build_character(character_data)
        assert not hasattr(character, "actual_stamina")

    def test_good_character_numeric_alignment_value(self, good_character):
        good_character = good_character
        assert good_character.alignment == 1

    def test_bad_character_numeric_alignment_value(self, bad_character):
        bad_character = bad_character
        assert bad_character.alignment == -1

    def test_correct_health_power_success(self, good_character, good_character_stats):
        character = good_character
        character_stats = good_character_stats
        correct_theoretical_health_points = (
            math.floor(
                (
                    (
                        (character_stats["strength"] * 0.8)
                        + (character_stats["durability"] * 0.7)
                        + character_stats["power"]
                    )
                    / 2
                )
                * (1 + (character_stats["actual_stamina"] / 10))
            )
            + 100
        )
        assert hasattr(character, "HP")
        actual_health_points = character.HP
        assert correct_theoretical_health_points == actual_health_points

    def test_correct_health_power_fail(self, good_character, good_character_stats):
        character = good_character
        character_stats = good_character_stats
        wrong_theoretical_health_points = (
            math.floor(
                (
                    (
                        (character_stats["strength"] * 1000)
                        + (character_stats["durability"] * 0.3)
                        + character_stats["power"]
                    )
                    / 2
                )
                * (1 + (character_stats["actual_stamina"] / 25))
            )
            + 100
        )
        assert hasattr(character, "HP")
        actual_health_points = character.HP
        assert not wrong_theoretical_health_points == actual_health_points

    def test_set_team_membership(self,good_character, random_id):
        character = good_character    
        character.set_team_membership(random_id)
        assert character.team_membership == random_id
