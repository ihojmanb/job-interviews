"""
conftest.py for test_characters
"""
import pytest
from ..conftest import*

# 

@pytest.fixture
def number_of_characters():
    return 731

@pytest.fixture()
def number_of_ids():
    return int(10)
    
@pytest.fixture(autouse=True)
def random_id(superhero_consumer):
    return superhero_consumer.get_random_id()

@pytest.fixture
def random_id_list(number_of_ids, superhero_consumer):
    return superhero_consumer.get_list_of_ids(number_of_ids)

@pytest.fixture
def good_character(character_factory):
    batman_data = load_fixture_character("good")
    batman = character_factory.build_character(batman_data)
    return batman

@pytest.fixture
def bad_character(character_factory):
    joker_data =  load_fixture_character("bad")
    joker = character_factory.build_character(joker_data)
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
        "HP": character.health_points
    }