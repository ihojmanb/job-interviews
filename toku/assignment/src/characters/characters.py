from fightclub_setup.superhero_api import *
import random
import math

class Character:
    def __init__(self, character_attributes) -> None:
        self.set_stats(character_attributes)
        self.set_alignment(character_attributes)
        self.set_actual_stamina()
        self.set_health_points()

    def set_health_points(self):
        health_points = (
            math.floor(
                (
                    (
                        (self.strength * 0.8)
                        + (self.durability * 0.7)
                        + self.power
                    )
                    / 2
                )
                * (1 + (self.actual_stamina / 10))
            )
            + 100
        )
        self.__setattr__("HP", health_points)

    def set_actual_stamina(self):
        self.__setattr__("actual_stamina", Character.random_stamina())
    
    def set_stats(self, attributes):
        powerstats = attributes["powerstats"]
        for stat, power in powerstats.items():
            # Setting stats attributes as ints
            self.__setattr__(stat, int(power) if power != 'null' else 0)
            # Setting actual stamina per stat
            self.__setattr__(f'AS_{stat}', Character.random_stamina())
    
    def set_alignment(self, attributes):
        alignment = attributes["biography"]["alignment"]
        # mapping aligment to numerical values
        self.__setattr__("alignment", 1 if alignment == 'good' else -1)
    
    def attack(self):
        pass

    @staticmethod
    def random_stamina():
        return random.randint(0, 10)


# Returns a Character object if id > 0, else returns None
def build_character(id):
    if id > 0:
        character_data = get_character(id)
        return Character(character_data)
    else:
        return None