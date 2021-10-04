import math
import random
import pytest
from functools import reduce
from characters.characters import *
from teams.teams import *
from tests.test_teams.conftest import bad_team, fixture_team, good_team
from fixture_team.fixture_team_loader import *
import utils.seed_handler as seed_handler
seed = seed_handler.load_seed()
random.seed(seed)

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

# Tests to verify that team and character communicate correctly

    def test_team_notifies_membership_to_characters(self):
        fixture_team = load_fixture_team()
        team = TeamCreator.build_team(fixture_team)
        assert hasattr(team, "id")
        for team_member in team.members:
            assert team_member.team_membership == team.id

    def test_team_notifies_alignment_to_characters(self):
        fixture_team = load_fixture_team()
        team = TeamCreator.build_team(fixture_team)
        for team_member in team.members:
            assert team_member.stats_updated == True

    def test_team_members_update_stats_success(self):
        fixture_team = load_fixture_team()
        team = TeamCreator.build_team(fixture_team)
        for character in team.members:
            assert character.stats_updated == True

    def test_team_members_update_stats_fail(self):
        fixture_team = load_fixture_team()
        list_of_characters_without_team = list(
            map(lambda character_data: build_character(character_data), fixture_team)
        )
        for character in list_of_characters_without_team:
            assert character.stats_updated == False

    # This test is to verify that the computation of the new stats is correct
    def test_team_members_update_stats_correctly(self):
        # load fixture team
        fixture_team = load_fixture_team()
        # build characters without a registered team
        list_of_characters_without_team = list(
            map(lambda character_data: build_character(character_data), fixture_team)
        )
        # now build a team with the same characters from fixture_team
        team_to_test = TeamCreator.build_team(fixture_team)
    
        # the characters in the team will have different stamina_stats given
        # our implementation. In order to compare them with the same characters
        # without team, lets set lets 
        # copy actual_stamina_stats from 'team_to_test' to 'list_of_characters_without_team'
        for index, character in enumerate(team_to_test.members):
            for stat in attributes:
                stamina_stat = character.__getattribute__(f'AS_{stat}')
                list_of_characters_without_team[index].__setattr__(f'AS_{stat}', stamina_stat)

        # lets take a the first character of the list without team
        character = list_of_characters_without_team[0]

        updated_list_of_characters_without_team = []
        # now we updated the stats of the characters without team
        # that we want to verify later, according to the formula
        for index, character in enumerate(list_of_characters_without_team):
            fc = team_to_test.members[index].fc
            for stat in attributes:
                old_stat = character.__getattribute__(stat)
                actual_stamina_stat = character.__getattribute__(f"AS_{stat}")
                updated_stat = math.floor(
                    (2 * old_stat + actual_stamina_stat) * fc / (1.1)
                )
                character.__setattr__(stat, updated_stat)
            updated_list_of_characters_without_team.append(character)

        # tests that the  stats of a character with no team when updated with
        # the correct formula are equal to the stats of the same character
        # that has a team that updates its stats automatically
        for index, character in enumerate(updated_list_of_characters_without_team):
            for stat in attributes:
                assert character.__getattribute__(stat) == team_to_test.members[
                    index
                ].__getattribute__(stat)
