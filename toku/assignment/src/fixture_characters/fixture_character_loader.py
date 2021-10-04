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
