import pytest
import pathlib
import os
import json

def load_fixture_team():
    current_file_path = pathlib.Path(__file__).parent.resolve()
    fixture_team_file_path = os.path.join(current_file_path, "fixture_team.json")
    fixture_team_file = open(fixture_team_file_path)
    fixture_team_json = json.load(fixture_team_file)
    list_of_fixture_team_characters = fixture_team_json["team"]
    return list_of_fixture_team_characters