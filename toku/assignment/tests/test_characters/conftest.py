"""
conftest.py for test_characters
"""
from fightclub_setup.superhero_api import *
from characters.characters import *
import pytest


@pytest.fixture
def number_of_characters():
    return 731

@pytest.fixture()
def number_of_ids():
    return int(10)
    
@pytest.fixture(autouse=True)
def random_id():
    return get_random_id()

@pytest.fixture
def random_id_list(number_of_ids):
    return get_list_of_ids(number_of_ids)

@pytest.fixture
def good_character():
    batman_data = get_character(70)
    batman = build_character(batman_data)
    return batman

@pytest.fixture
def bad_character():
    joker_data = get_character(370)
    joker = build_character(joker_data)
    return joker

@pytest.fixture
def good_character_stats(good_character):
    character = good_character
    return {
        "intelligence": character.intelligence,
        "strength" : character.strength,
        "durability" : character.durability,
        "power" : character.power,
        "combat": character.combat,
        "actual_stamina" : character.actual_stamina,
        "HP": character.HP
    }