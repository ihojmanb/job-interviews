from ctypes import alignment
import math
import random
from functools import reduce
from typing import overload
from characters.characters import *
from fightclub_setup.superhero_api import *


class Team:
    def __init__(self, list_of_characters):
        self.set_team_members(list_of_characters)
        self.set_team_alignment()

    def set_team_members(self, list_of_characters):
        members = list(
            map(
                # build_character es poco claro, sería bueno tener
                # una clase que encapsulara el metodo y tener una instancia
                # de ella en Team
                lambda character: build_character(int(character["id"])),
                list_of_characters,
            )
        )
        self.__setattr__("members", members)

    def set_team_alignment(self):
        alignment_list = list(map(lambda m: m.alignment, self.members))
        team_alignment = reduce(lambda x, y: x + y, alignment_list)
        team_alignment = "good" if team_alignment > 0 else "bad"
        self.__setattr__("alignment", team_alignment)


# Falta testing en esta clase 
class TeamCreator:
    def __init__(self):
        pass

    @staticmethod
    def build_team(list_of_characters):
            return Team(list_of_characters)

    @staticmethod
    def build_random_team(number_of_team_members=5):
        if number_of_team_members > 0:
            list_of_characters = get_random_list_of_characters(number_of_team_members)
            return TeamCreator.build_team(list_of_characters)
        else:
            return None
