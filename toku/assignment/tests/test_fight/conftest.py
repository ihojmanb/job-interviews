"""
conftest.py for test_fight.py
"""
from fixture_team.fixture_team_loader import *
from teams.teams import TeamCreator
import pytest
from fixture_team.fixture_team_loader import *


@pytest.fixture
def fixture_team():
    return TeamCreator.build_random_team(number_of_team_members=5)

