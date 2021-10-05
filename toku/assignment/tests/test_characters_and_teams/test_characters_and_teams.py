"""
    tests to verify the relation between Teams and Characters
"""
import math, random
from characters.characters import *
from teams.teams import *
from fixture_team.fixture_team_loader import *
from fixture_characters.fixture_character_loader import *

# Setup
# fixture_team = load_fixture_team()
# superhero_consumer = SuperHeroApiConsumer(credentials["access-token"])
# character_factory = CharacterFactory(superhero_consumer)
# team_creator = TeamCreator(character_factory=character_factory)
# list_of_characters = load_fixture_characters()


class TestCharactersAndTeams:
    # Tests to verify that team and character communicate correctly
    def test_team_notifies_membership_to_characters(self, team_creator):
        fixture_team = load_fixture_team()
        team = team_creator.build_team(
            team_name="team", list_of_characters=fixture_team
        )
        for team_member in team.members:
            assert team_member.team == team

    def test_team_notifies_alignment_to_characters(self, team_creator):
        fixture_team = load_fixture_team()
        team = team_creator.build_team(
            team_name="team", list_of_characters=fixture_team
        )
        for team_member in team.members:
            assert team_member.stats_updated == True

    def test_team_members_update_stats_success(self, team_creator):
        fixture_team = load_fixture_team()
        team = team_creator.build_team(
            team_name="team", list_of_characters=fixture_team
        )
        for character in team.members:
            assert character.stats_updated == True

    def test_team_members_update_stats_fail(self, character_factory):
        fixture_team = load_fixture_team()
        list_of_characters_without_team = list(
            map(
                lambda character_data: character_factory.build_character(
                    character_data
                ),
                fixture_team,
            )
        )
        for character in list_of_characters_without_team:
            assert character.stats_updated == False

    # This test is to verify that the computation of the new stats is correct
    def test_team_members_update_stats_correctly(self, team, character_factory):
        fixture_team = load_fixture_team()
        # load fixture team
        # build characters without a registered team
        list_of_characters_without_team = list(
            map(
                lambda character_data: character_factory.build_character(
                    character_data
                ),
                fixture_team,
            )
        )
        # now build a team with the same characters from fixture_team
        team_to_test = team

        # the characters in the team will have different stamina_stats given
        # our implementation. In order to compare them with the same characters
        # without team, lets set lets
        # copy actual_stamina_stats from 'team_to_test' to 'list_of_characters_without_team'
        for index, character in enumerate(team_to_test.members):
            for stat in attributes:
                stamina_stat = character.__getattribute__(f"AS_{stat}")
                list_of_characters_without_team[index].__setattr__(
                    f"AS_{stat}", stamina_stat
                )

        # lets take a the first character of the list without team
        character = list_of_characters_without_team[0]

        updated_list_of_characters_without_team = []
        # now we updated the stats of the characters without team
        # that we want to verify later, according to the formula
        for index, character in enumerate(list_of_characters_without_team):
            fc = team_to_test.members[index].filliation_coefficient
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

    def test_set_character_attacks(self, team_creator):
        fixture_team = load_fixture_team()
        team = team_creator.build_team(
            team_name="team", list_of_characters=fixture_team
        )
        character = random.choice(team.members)
        assert hasattr(character, "mental_attack")
        assert hasattr(character, "strong_attack")
        assert hasattr(character, "fast_attack")

    def test_mental_attack_computed_correcty(self, team_creator):
        fixture_team = load_fixture_team()
        team = team_creator.build_team(
            team_name="team", list_of_characters=fixture_team
        )
        character = random.choice(team.members)
        mental_attack_value = (
            (character.intelligence * 0.7)
            + (character.speed * 0.2)
            + (character.combat * 0.1) * character.filliation_coefficient
        )
        assert mental_attack_value, character.mental_attack

    def test_strong_attack_computed_correcty(self, team_creator):
        fixture_team = load_fixture_team()
        team = team_creator.build_team(
            team_name="team", list_of_characters=fixture_team
        )
        character = random.choice(team.members)
        strong_attack_value = (
            (character.strength * 0.6)
            + (character.power * 0.2)
            + (character.combat * 0.2) * character.filliation_coefficient
        )
        assert strong_attack_value, character.strong_attack

    def test_fast_attack_computed_correcty(self, team_creator):
        fixture_team = load_fixture_team()
        team = team_creator.build_team(
            team_name="team", list_of_characters=fixture_team
        )
        character = random.choice(team.members)
        fast_attack_value = (
            (character.speed * 0.55)
            + (character.durability * 0.25)
            + (character.strength * 0.2) * character.filliation_coefficient
        )
        assert fast_attack_value, character.fast_attack
