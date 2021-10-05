"""
conftest.py for every test_*.py
"""
import pytest
import json
from superhero.superhero_api import SuperHeroApiConsumer
from characters.characters import CharacterFactory
from teams.teams import TeamCreator
from fixture_characters.fixture_character_loader import *
from fixture_team.fixture_team_loader import load_fixture_team

fixture_team = load_fixture_team()

@pytest.fixture
def credentials():
    credentials = open("credentials.json")
    credentials = json.load(credentials)
    return credentials

@pytest.fixture
def superhero_consumer(credentials):
    superhero_consumer = SuperHeroApiConsumer(credentials["access-token"])
    return superhero_consumer

@pytest.fixture
def character_factory(superhero_consumer):
    character_factory = CharacterFactory(superhero_consumer)
    return character_factory

@pytest.fixture
def team(team_creator):
    team = team_creator.build_team("team_name",fixture_team)
    return team

@pytest.fixture
def team_creator(character_factory):
    return TeamCreator(character_factory)

