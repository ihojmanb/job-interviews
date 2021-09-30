import json
import requests
import random

credentials = open('credentials.json')
credentials = json.load(credentials)
base_url = f'https://superheroapi.com/api/{credentials["access-token"]}'
# generate 10 unique id's between 1 and 731
def get_list_of_ids():
    list_of_ids = random.sample(range(1, 731), k=10)
    return list_of_ids

# returns a list with 1 random id
def get_random_id():
    random_id= random.randint(1, 731)
    return random_id

def get_list_of_characters(number_of_characters):
    # url = f'https://superheroapi.com/api/{credentials["access-token"]}/'
    # return url
    pass


def get_character(id):
    character_url = f'{base_url}/{id}'
    character_response = requests.get(character_url)
    character_object = character_response.json()
    return character_object


if __name__ == "__main__":
    # pass
    print(get_list_of_characters(1))