import random
import string
from functools import reduce
from characters.characters import *
from base_component.base_component import *


class Team(BaseComponent):
    def __init__(self, name, list_of_characters, character_factory: CharacterFactory):
        self._name = name
        self._character_factory = character_factory
        self.set_team_members(list_of_characters)
        self.set_team_alignment()
        self._actual_fighter = self.members[0]

    @property
    def name(self):
        return self._name

    @property
    def character_factory(self):
        return self._character_factory

    @property
    def actual_fighter(self):
        return self._actual_fighter

    @actual_fighter.setter
    def actual_fighter(self, new_fighter):
        self._actual_fighter = new_fighter

    @actual_fighter.deleter
    def actual_fighter(self):
        del self._actual_fighter

    def set_team_members(self, list_of_characters):
        members = list(
            map(
                lambda character: self.character_factory.build_character(character),
                list_of_characters,
            )
        )
        self.members = members
        self.notify("membership")

    def set_team_alignment(self):
        alignment_list = list(map(lambda m: m.alignment, self.members))
        team_alignment = reduce(lambda x, y: x + y, alignment_list)
        team_alignment = "good" if team_alignment > 0 else "bad"
        self.alignment = team_alignment
        self.notify("alignment")

    def attack(self, type_of_attack):
        if self.actual_fighter.health_points > 0:
            attack_damage = self.actual_fighter.attack(type_of_attack)
            self.mediator.notify_attack(self, attack_damage)

    def receive_damage(self, damage):
        self.actual_fighter.receive_damage(damage)

    # Observer Pattern with team_members (as Publisher)
    def notify(self, event):
        if event == "membership":
            for team_member in self.members:
                team_member.team = self

        elif event == "alignment":
            for team_member in self.members:
                team_member.update_stats(self.alignment)

    # Observer Pattern with team members (as Subscriber)
    def update(self, character: Character) -> None:
        if character.health_points == 0 and character == self.actual_fighter:
            if len(self.members) > 1:
                self.mediator.notify_defeat(character)
                self.members.pop(0)
                new_actual_fighter = self.members[0]
                self.actual_fighter = new_actual_fighter

            elif len(self.members) == 1:
                self.mediator.notify_defeat(character)
                self.members.pop(0)
                self.mediator.notify_end_fight(self)
            else:
                self.mediator.notify_defeat(character)     
                self.mediator.notify_end_fight(self)


# Falta testing de esta clase
class TeamCreator:
    def __init__(self, character_factory: CharacterFactory):
        self._character_factory = character_factory
        self._unavailable_team_names = []

    @property
    def character_factory(self):
        return self._character_factory

    @property
    def unavailable_names(self):
        return self._unavailable_team_names

    def build_team(self, team_name, list_of_characters):
        if team_name not in self.unavailable_names:
            team = Team(team_name, list_of_characters, self.character_factory)
            self.unavailable_names.append(team_name)
            return team
        else:
            raise Exception(
                "El nombre que elegiste ya está en uso, por favor escoge otro"
            )

    def build_random_team(self,team_name, number_of_team_members=5):
        if number_of_team_members > 0:
            list_of_characters = self.character_factory.get_list_of_characters(
                number_of_team_members
            )
            return self.build_team(team_name, list_of_characters)
        else:
            return None
