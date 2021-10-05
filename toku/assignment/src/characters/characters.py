import random
import math
from superhero.superhero_api import *
from base_component.base_component import *

attributes = ["intelligence", "strength", "speed", "durability", "power", "combat"]


class Character:
    def __init__(self, character_attributes) -> None:
        self.set_character(character_attributes)

    def set_character(self, character_attributes):
        self.set_name(character_attributes["name"])
        self.set_id(character_attributes["id"])
        self.set_stats(character_attributes)
        self.set_alignment(character_attributes)
        self.set_actual_stamina()
        self._health_points = self.__init_health_points()
        self._stats_updated = False
        self._team = None
    
    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, updated_health_points):
        self._health_points = updated_health_points

    @property
    def stats_updated(self):
        return self._stats_updated

    @stats_updated.setter
    def stats_updated(self, new_value):
        self._stats_updated = new_value


    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, team):
        self._team = team


    # Setters
    def set_name(self, name):
        self.__setattr__("name", name)

    def set_id(self, id):
        self.__setattr__("id", id)

    def set_stats(self, attributes):

        powerstats = attributes["powerstats"]
        for stat, power in powerstats.items():
            # Setting stats attributes as ints
            self.__setattr__(stat, int(power) if power != "null" else 0)
            # Setting actual stamina per stat
            stamina = self.stamina()
            self.__setattr__(f"AS_{stat}", stamina)

    def set_alignment(self, attributes):
        alignment = attributes["biography"]["alignment"]
        # mapping aligment to numerical values
        self.__setattr__("alignment", 1 if alignment == "good" else -1)

    def set_actual_stamina(self):
        self.__setattr__("actual_stamina", self.stamina())

#   health points initializer (private method)
    def __init_health_points(self):
        health_points = (
            math.floor(
                (((self.strength * 0.8) + (self.durability * 0.7) + self.power) / 2)
                * (1 + (self.actual_stamina / 10))
            )
            + 100
        )
        return health_points



    def set_team_membership(self, team_id):
        self.__setattr__("team_membership", team_id)

    def update_stats(self, team_alignment):
        self.set_filliation_coefficient(team_alignment)
        for stat in attributes:
            old_stat = self.__getattribute__(stat)
            actual_stamina_stat = self.__getattribute__(f"AS_{stat}")
            updated_stat = math.floor(
                ((2 * old_stat) + actual_stamina_stat)
                * self.filliation_coefficient
                / (1.1)
            )
            self.__setattr__(stat, updated_stat)
        self.__setattr__("stats_updated", True)
        self.set_attacks()

    def set_filliation_coefficient(self, team_alignment):
        fc = self.calculate_filliation_coefficient(team_alignment)
        self.__setattr__("filliation_coefficient", fc)

    def set_attacks(self):
        self.set_mental_attack()
        self.set_strong_attack()
        self.set_fast_attack()

    def set_mental_attack(self):
        mental_attack_value = (
            (self.intelligence * 0.7)
            + (self.speed * 0.2)
            + (self.combat * 0.1) * self.filliation_coefficient
        )
        self.__setattr__("mental_attack", mental_attack_value)

    def set_strong_attack(self):
        strong_attack_value = (
            (self.strength * 0.6)
            + (self.power * 0.2)
            + (self.combat * 0.2) * self.filliation_coefficient
        )
        self.__setattr__("strong_attack", strong_attack_value)

    def set_fast_attack(self):
        fast_attack_value = (
            (self.speed * 0.55)
            + (self.durability * 0.25)
            + (self.strength * 0.2) * self.filliation_coefficient
        )
        self.__setattr__("fast_attack", fast_attack_value)

    # Getters
    def get_stats(self):
        stats_dict = {}
        for stat in attributes:
            stats_dict[stat] = self.__getattribute__(stat)
        return stats_dict

    def get_stamina_stats(self):
        stamina_stats_dict = {}
        for stat in attributes:
            stamina_stats_dict[f"AS_{stat}"] = self.__getattribute__(f"AS_{stat}")
        return stamina_stats_dict

    # Auxiliary methods
    def calculate_filliation_coefficient(self, team_alignment):
        numerical_team_alignment = 1 if team_alignment == "good" else -1
        coefficient = 1 + random.randrange(10)
        if self.alignment == numerical_team_alignment:
            return coefficient
        else:
            return math.pow(coefficient, -1)

    def stamina(self):
        random_stamina = random.randint(0, 10)
        return random_stamina

    # Business Logic
    def attack(self, type_of_attack):
        if type_of_attack == "mental_attack":
            return self.mental_attack
        elif type_of_attack == "strong_attack":
            return self.strong_attack
        elif type_of_attack == "fast_attack":
            return self.fast_attack

    def receive_damage(self, damage):
        old_health_points = self.health_points
        new_health_points = old_health_points - damage
        if new_health_points > 0:
            self.health_points = new_health_points 
        else:
            self.health_points = 0
            self.team.update(self)


class CharacterFactory:
    def __init__(self, api_consumer: SuperHeroApiConsumer):
        self._api_consumer = api_consumer

    @property
    def api_consumer(self):
        return self._api_consumer

    def get_list_of_characters(self, number_of_characters):
        list_of_characters = self.api_consumer.get_random_list_of_characters(
            number_of_characters=number_of_characters
        )
        return list_of_characters
    

    def build_character(self, character_data):
        if character_data["response"] == "success":
            return Character(character_data)
        else:
            return None

    def build_characters(self, list_of_characters):
        built_characters = list(
            map(lambda character: self.build_character(character), list_of_characters)
        )
        return built_characters
