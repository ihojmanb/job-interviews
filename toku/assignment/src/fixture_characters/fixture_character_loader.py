import pathlib
import os
import json


def load_fixture_character(alignment):
    current_file_path = pathlib.Path(__file__).parent.resolve()
    fixture_character_file_path = os.path.join(
        current_file_path, f"{alignment}_character.json"
    )
    fixture_character_file = open(fixture_character_file_path)
    fixture_character_json = json.load(fixture_character_file)
    return fixture_character_json


def load_fixture_characters():
    current_file_path = pathlib.Path(__file__).parent.resolve()
    fixture_characters_file_path = os.path.join(
        current_file_path, "characters.json"
    )
    fixture_characters_file = open(fixture_characters_file_path)
    fixture_characters_json = json.load(fixture_characters_file)
    list_of_fixture_characters = fixture_characters_json["characters"]
    return list_of_fixture_characters