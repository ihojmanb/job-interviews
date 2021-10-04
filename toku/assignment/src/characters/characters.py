from fightclub_setup.superhero_api import *
import random
import math
import utils.seed_handler as seed_handler

# seed = seed_handler.load_seed()
# random.seed(seed)
# seed = int("DEADBEEF", 16)
# random.seed(seed)
# seed_handler.save_seed(seed)


attributes = ["intelligence", "strength", "speed", "durability", "power", "combat"]


class Character:
    def __init__(self, character_attributes) -> None:
        self.set_name(character_attributes["name"])
        self.set_id(character_attributes["id"])
        self.set_stats(character_attributes)
        self.set_alignment(character_attributes)
        self.set_actual_stamina()
        self.set_health_points()
        self.__setattr__("stats_updated", False)

    def set_name(self, name):
        self.__setattr__("name", name)

    def set_id(self, id):
        self.__setattr__("id", id)

    def set_health_points(self):
        health_points = (
            math.floor(
                (((self.strength * 0.8) + (self.durability * 0.7) + self.power) / 2)
                * (1 + (self.actual_stamina / 10))
            )
            + 100
        )
        self.__setattr__("HP", health_points)

    def set_actual_stamina(self):
        self.__setattr__("actual_stamina", self.stamina())

    def set_stats(self, attributes):

        powerstats = attributes["powerstats"]
        for stat, power in powerstats.items():
            # Setting stats attributes as ints
            self.__setattr__(stat, int(power) if power != "null" else 0)
            # Setting actual stamina per stat
            stamina = self.stamina()
            self.__setattr__(f"AS_{stat}", stamina)

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

    def set_alignment(self, attributes):
        alignment = attributes["biography"]["alignment"]
        # mapping aligment to numerical values
        self.__setattr__("alignment", 1 if alignment == "good" else -1)

    def set_team_membership(self, team_id):
        self.__setattr__("team_membership", team_id)

    def update_stats(self, team_alignment):
        fc = self.calculate_filliation_coefficient(team_alignment)
        self.__setattr__("fc", fc)
        for stat in attributes:
            old_stat = self.__getattribute__(stat)
            actual_stamina_stat = self.__getattribute__(f"AS_{stat}")
            updated_stat = math.floor(
                ((2 * old_stat) + actual_stamina_stat) * fc / (1.1)
            )
            self.__setattr__(stat, updated_stat)
        self.__setattr__("stats_updated", True)

    def calculate_filliation_coefficient(self, team_alignment):
        numerical_team_alignment = 1 if team_alignment == "good" else -1
        coefficient = 1 + random.randrange(10)
        # coefficient = 1
        if self.alignment == numerical_team_alignment:
            return coefficient
        else:
            return math.pow(coefficient, -1)

    def attack(self):
        pass

    def stamina(self):
        random_stamina = random.randint(0, 10)
        return random_stamina


# Returns a Character object if character_data['response'] == 'success',
#  else returns None
def build_character(character_data):
    if character_data["response"] == "success":
        return Character(character_data)
    else:
        return None
