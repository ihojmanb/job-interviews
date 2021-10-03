import math
import random
import pytest
from characters.characters import *
from teams.teams import *
from tests.test_teams.conftest import bad_team, good_team

class TestTeams:
    def test_build_team_success(self, number_of_team_members):
        team = TeamCreator.build_random_team(number_of_team_members)
        assert team
        assert isinstance(team, Team)
        assert len(team.members) == number_of_team_members

    def test_build_team_fail(self):
        team = TeamCreator.build_random_team(0)
        assert not isinstance(team, Team)

    def test_team_alignment_good_success(self, good_team):
        team = good_team
        assert isinstance(team, Team)
        assert team.alignment == 'good'

    def test_team_alignment_good_fail(self, bad_team):
        team = bad_team
        assert isinstance(team, Team)
        assert not team.alignment == 'good'

    def test_team_alignment_bad_success(self, bad_team):
        team = bad_team
        assert isinstance(team, Team)
        assert team.alignment == 'bad'

    def test_team_alignment_bad_fail(self, good_team):
        team = good_team
        assert isinstance(team, Team)
        assert not team.alignment == 'bad'
