#!/usr/bin/env python3
import json
import requests
import random

# setup
credentials = open("credentials.json")
credentials = json.load(credentials)
base_url = f'https://superheroapi.com/api/{credentials["access-token"]}'
total_number_of_characters = 731


def get_random_id():
    random_id = random.randint(1, total_number_of_characters)
    return random_id


# generates 'number_of_ids' unique id's between 1 and total_number_of_characters
def get_list_of_ids(number_of_ids):
    list_of_ids = random.sample(range(1, total_number_of_characters), k=number_of_ids)
    return list_of_ids


def get_character(id):
    character_url = f"{base_url}/{id}"
    character_response = requests.get(character_url)
    character_object = character_response.json()
    return character_object



def get_random_list_of_characters(number_of_characters):
    list_of_ids = get_list_of_ids(number_of_characters)
    random_list_of_characters = list(map(lambda id: get_character(id), list_of_ids))
    return random_list_of_characters