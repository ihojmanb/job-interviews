import pytest
import random
from fight import *
from fight import fight_mediator
from fight.fight import FightAdmin, FightEnded, FightNotStarted, FightStarted
from fight.fight_mediator import FightMediator
from fixture_characters.fixture_character_loader import load_fixture_characters
from teams.teams import *
from fixture_characters.fixture_character_loader import *

# Setup
superhero_consumer = SuperHeroApiConsumer(credentials["access-token"])
character_factory = CharacterFactory(superhero_consumer)

list_of_characters = load_fixture_characters()


class TestFightMediator:

    def test_fight_mediator_registers_correctly_to_teams(self):
        team_creator = TeamCreator(character_factory=character_factory)
        team2 = team_creator.build_team(team_name='team2', list_of_characters=list_of_characters[5:])
        team1 = team_creator.build_team(team_name='team1', list_of_characters=list_of_characters[0:5])
        fight_mediator = FightMediator(team1, team2)
        assert isinstance(team1.mediator, FightMediator)
        assert isinstance(team2.mediator, FightMediator)
        assert fight_mediator == team1.mediator
        assert fight_mediator == team2.mediator

    def test_fight_mediator_delivers_message_from_1_to_2(self):
        team_creator = TeamCreator(character_factory=character_factory)
        team1 = team_creator.build_team(team_name='team1', list_of_characters=list_of_characters[0:5])
        team2 = team_creator.build_team(team_name='team2', list_of_characters=list_of_characters[5:])
        fight_mediator = FightMediator(team1, team2)
        fighter1 = team1.actual_fighter
        fighter2 = team2.actual_fighter
        fighter2_old_health_points = fighter2.health_points
        team1.attack("mental_attack")
        assert (
            fighter2_old_health_points - fighter1.mental_attack
        ) <= fighter2.health_points

    def test_fight_mediator_delivers_message_from_2_to_1(self):
        team_creator = TeamCreator(character_factory=character_factory)
        team1 = team_creator.build_team(team_name='team1', list_of_characters=list_of_characters[0:5])
        team2 = team_creator.build_team(team_name='team2', list_of_characters=list_of_characters[5:])
        fight_mediator = FightMediator(team1, team2)
        fighter1 = team1.actual_fighter
        fighter2 = team2.actual_fighter
        fighter1_old_health_points = fighter1.health_points
        team2.attack("fast_attack")
        assert (
            fighter1_old_health_points - fighter2.fast_attack
        ) <= fighter1.health_points


class TestFight:
    def test_fight_mediator_has_fight_admin(self):
        team_creator = TeamCreator(character_factory=character_factory)
        team1 = team_creator.build_team(team_name='team1', list_of_characters=list_of_characters[0:5])
        team2 = team_creator.build_team(team_name='team2', list_of_characters=list_of_characters[5:])
        fight_mediator = FightMediator(team1, team2)
        fight_admin = FightAdmin(fight_mediator)
        assert isinstance(fight_mediator.admin, FightAdmin)

    def test_team2_changes_its_actual_fighter(self):
        team_creator = TeamCreator(character_factory=character_factory)
        team1 = team_creator.build_team(team_name='team1', list_of_characters=list_of_characters[0:5])
        team2 = team_creator.build_team(team_name='team2', list_of_characters=list_of_characters[5:])
        fight_mediator = FightMediator(team1, team2)
        fighter1 = team1.actual_fighter
        fighter2 = team2.actual_fighter
        fighter2_health_points = fighter2.health_points
        while fighter2.health_points > 0:
            team1.attack("strong_attack")

        assert fighter2.health_points == 0
        assert fighter2 != team2.actual_fighter


    def test_team1_wins_over_team2(self):
        team_creator = TeamCreator(character_factory=character_factory)
        team1 = team_creator.build_team(team_name='team1', list_of_characters=list_of_characters[0:5])
        team2 = team_creator.build_team(team_name='team2', list_of_characters=list_of_characters[5:])
        fight_mediator = FightMediator(team1, team2)
        fight_admin = FightAdmin(fight_mediator)

        while len(team2.members) > 0 and team2.actual_fighter.health_points > 0:
            team1.attack("mental_attack")
        assert len(team2.members) == 0
        assert fight_admin.winner == team1


    def test_fight_state_is_FightNotStarted(self):
        team_creator = TeamCreator(character_factory=character_factory)
        team1 = team_creator.build_team(team_name='team1', list_of_characters=list_of_characters[0:5])
        team2 = team_creator.build_team(team_name='team2', list_of_characters=list_of_characters[5:])
        fight_mediator = FightMediator(team1, team2)
        fight_admin = FightAdmin(fight_mediator)
        assert isinstance(fight_admin.state, FightNotStarted)

    def test_fight_state_transition_from_FightNotStarted_to_FightStarted(self):
        team_creator = TeamCreator(character_factory=character_factory)
        team1 = team_creator.build_team(team_name='team1', list_of_characters=list_of_characters[0:5])
        team2 = team_creator.build_team(team_name='team2', list_of_characters=list_of_characters[5:])
        fight_mediator = FightMediator(team1, team2)
        fight_admin = FightAdmin(fight_mediator)
        assert isinstance(fight_admin.state, FightNotStarted)      
        fight_admin.start_fight()
        assert isinstance(fight_admin.state, FightStarted)

    def test_fight_state_transition_from_FightNotStarted_to_FightEnded(self):
        team_creator = TeamCreator(character_factory=character_factory)
        team1 = team_creator.build_team(team_name='team1', list_of_characters=list_of_characters[0:5])
        team2 = team_creator.build_team(team_name='team2', list_of_characters=list_of_characters[5:])
        fight_mediator = FightMediator(team1, team2)
        fight_admin = FightAdmin(fight_mediator)
        assert isinstance(fight_admin.state, FightNotStarted)      
        fight_admin.end_fight()
        assert isinstance(fight_admin.state, FightEnded)

    def test_fight_state_transition_from_FightStarted_to_FightEnded(self):
        team_creator = TeamCreator(character_factory=character_factory)
        team1 = team_creator.build_team(team_name='team1', list_of_characters=list_of_characters[0:5])
        team2 = team_creator.build_team(team_name='team2', list_of_characters=list_of_characters[5:])
        fight_mediator = FightMediator(team1, team2)
        fight_admin = FightAdmin(fight_mediator)
        assert isinstance(fight_admin.state, FightNotStarted)      
        fight_admin.start_fight()
        assert isinstance(fight_admin.state, FightStarted)
        fight_admin.end_fight()
        assert isinstance(fight_admin.state, FightEnded)

    def test_fight_admin_gets_notified_of_ended_fight(self):
        team_creator = TeamCreator(character_factory=character_factory)
        team1 = team_creator.build_team(team_name='team1', list_of_characters=list_of_characters[0:5])
        team2 = team_creator.build_team(team_name='team2', list_of_characters=list_of_characters[5:])
        fight_mediator = FightMediator(team1, team2)
        fight_admin = FightAdmin(fight_mediator)
        attack_choice = ['mental_attack', 'strong_attack', 'fast_attack']
        while len(team1.members) > 0 and len(team2.members) > 0:
            team1.attack(random.choice(attack_choice))
            team2.attack(random.choice(attack_choice))
        print(f'winner:{fight_admin.winner.name}')
        assert isinstance(fight_admin.state, FightEnded)

    def test_raise_exception_when_teams_have_the_same_name(self):
        team_creator = TeamCreator(character_factory=character_factory)
        team1 = team_creator.build_team(team_name='team1', list_of_characters=list_of_characters[0:5])
        with pytest.raises(Exception) as e_info:
            assert team_creator.build_team(team_name='team1', list_of_characters=list_of_characters[5:])
            assert e_info == "El nombre que elegiste ya está en uso, por favor escoge otro"