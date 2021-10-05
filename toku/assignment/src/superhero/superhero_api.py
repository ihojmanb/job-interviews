#!/usr/bin/env python3
import json
import requests
import random

# setup
credentials = open("credentials.json")
credentials = json.load(credentials)
base_url = f'https://superheroapi.com/api/{credentials["access-token"]}'

class SuperHeroApiConsumer:
    def __init__(self, access_token):
        self._total_number_of_characters = 731
        self._access_token = access_token
        self._base_url = f'https://superheroapi.com/api/{self.access_token}'
    
    @property
    def total_number_of_characters(self):
        return self._total_number_of_characters
    @property
    def access_token(self):
        return self._access_token
    @property
    def base_url(self):
        return self._base_url

    def get_list_of_ids(self, number_of_ids):
        list_of_ids = random.sample(range(1, self.total_number_of_characters), k=number_of_ids)
        return list_of_ids
    
    def get_character(self, id):
        character_url = f"{self.base_url}/{id}"
        character_response = requests.get(character_url)
        character_object = character_response.json()
        return character_object

    def get_random_list_of_characters(self, number_of_characters):
        list_of_ids = self.get_list_of_ids(number_of_characters)
        random_list_of_characters = list(map(lambda id: self.get_character(id), list_of_ids))
        return random_list_of_characters

    def get_random_id(self):
        random_id = random.randint(1, self.total_number_of_characters)
        return random_id
