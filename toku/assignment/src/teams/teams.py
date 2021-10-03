from ctypes import alignment
import math
import random
from functools import reduce
from characters.characters import *
from fightclub_setup.superhero_api import *

class Team:
    def __init__(self, number_of_team_members):
        list_of_characters = get_random_list_of_characters(number_of_team_members)
        self.set_team_members(list_of_characters)
        self.set_team_alignment()

    def set_team_members(self, list_of_characters):
        members = list(map(lambda character: build_character(int(character['id'])), list_of_characters))
        self.__setattr__('members', members)

    def set_team_alignment(self):
        alignment_list = list(map(lambda m: m.alignment, self.members))
        team_alignment = reduce(lambda x, y: x + y, alignment_list)
        team_alignment = 'good' if team_alignment > 0 else 'bad'
        self.__setattr__('alignment', team_alignment)

def build_team(number_of_team_members=5):
    if number_of_team_members > 0:
        return Team(number_of_team_members)
    else:
        return None