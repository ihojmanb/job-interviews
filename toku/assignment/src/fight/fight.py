from abc import abstractmethod
from fight.fight_mediator import FightMediator
import random


class FightState:
    def __init__(self, fight):
        self._fight = fight

    @property
    def fight(self):
        return self._fight

    @fight.setter
    def fight(self, fight):
        self._fight = fight

    @abstractmethod
    def handle_start_fight(self):
        pass

    @abstractmethod
    def handle_end_fight(self):
        pass


class FightNotStarted(FightState):
    def handle_start_fight(self):
        print("Fight started")
        self.fight.transition_to(FightStarted(self.fight))

    def handle_end_fight(self):
        print("Fight canceled")
        self.fight.transition_to(FightEnded(self.fight))


class FightStarted(FightState):
    def handle_end_fight(self):
        print("Fight ended")
        self.fight.transition_to(FightEnded(self.fight))


class FightEnded(FightState):
    pass


class FightAdmin:
    """
    FightAdmin Class manages the State of the current game:
    if it has not started, if it has started, it if has ended,
     how many characters each team has left, which characters
     participated in each fight, etc.

    Fight acts as context.

    """

    _winner = None
    _defeated_character = None

    def __init__(self, fight_mediator: FightMediator):
        self._state = FightNotStarted(self)
        self._fight_mediator = fight_mediator
        self._fight_mediator.admin = self
        self._teams = [self.fight_mediator.team1, self.fight_mediator.team2]

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    @property
    def fight_mediator(self):
        return self._fight_mediator

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, winner):
        self._winner = winner

    @property
    def defeated_character(self):
        return self._defeated_character

    @defeated_character.setter
    def defeated_character(self, defeated_character):
        self._defeated_character = defeated_character



    @property
    def teams(self):
        return self._teams

    @teams.setter
    def teams(self, teams):
        self._teams = teams


    def transition_to(self, state: FightState):
        self.state = state
        self.state.fight = self

    def start_fight(self):
        self.state.handle_start_fight()

    def end_fight(self):
        self.state.handle_end_fight()
