"""
conftest.py for test_characters_and_teams.py
"""
from teams.teams import TeamCreator
import pytest
from fixture_team.fixture_team_loader import *
from ..conftest import *

@pytest.fixture
def number_of_team_members():
    return int(5)


@pytest.fixture
def fixture_team():
    return TeamCreator.build_random_team(number_of_team_members=5)

@pytest.fixture
def good_team():
    team = TeamCreator.build_team(load_fixture_team())
    for index, character in enumerate(team.members):
        # if index is odd
        character.alignment = 1 if ((index + 1)%2 != 0) else -1
        team.members[index] = character
    # recalculate team alignment
    team.set_team_alignment()
    good_team = team
    return good_team

@pytest.fixture
def bad_team():
    team = TeamCreator.build_team(load_fixture_team())
    for index, character in enumerate(team.members):
        # if index is odd
        character.alignment = -1 if ((index + 1)%2 != 0) else 1
        team.members[index] = character
    # recalculate team alignment
    team.set_team_alignment()
    bad_team = team
    return bad_team

