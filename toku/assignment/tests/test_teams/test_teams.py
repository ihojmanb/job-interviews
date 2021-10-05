import math
from characters.characters import *
from teams.teams import *
from fixture_team.fixture_team_loader import *

attributes = ["intelligence", "strength", "speed", "durability", "power", "combat"]

class TestTeams:
    def test_build_team_success(self, number_of_team_members):
        fixture_team = load_fixture_team()
        team = TeamCreator.build_team(fixture_team)
        assert team
        assert isinstance(team, Team)
        assert len(team.members) == number_of_team_members

    def test_build_team_fail(self):
        team = TeamCreator.build_random_team(0)
        assert not isinstance(team, Team)

    def test_team_alignment_good_success(self, good_team):
        team = good_team
        assert isinstance(team, Team)
        assert team.alignment == "good"

    def test_team_alignment_good_fail(self, bad_team):
        team = bad_team
        assert isinstance(team, Team)
        assert not team.alignment == "good"

    def test_team_alignment_bad_success(self, bad_team):
        team = bad_team
        assert isinstance(team, Team)
        assert team.alignment == "bad"

    def test_team_alignment_bad_fail(self, good_team):
        team = good_team
        assert isinstance(team, Team)
        assert not team.alignment == "bad"

    def test_teams_have_different_ids(self, good_team, bad_team):
        good_team = good_team
        bad_team = bad_team
        assert good_team.id != bad_team.id
