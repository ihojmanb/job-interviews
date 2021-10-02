from os.path import join, dirname
import json
from jsonschema import validate
from fightclub_setup.superhero_api import *

def assert_valid_schema(data, schema_file):
    schema = _load_json_schema(schema_file)
    return validate(data, schema)

def _load_json_schema(filename):
    relative_path = join('schemas', filename)
    absolute_path = join(dirname(__file__), relative_path)

    with open(absolute_path) as schema_file:
        return json.loads(schema_file.read())

"""Testing the proper structure of the json object retrieve by the 
superhero api call"""

class TestSchema:
    def test_validate_character_data_schema(self):
        id = get_random_id()
        character = get_character(id)
        assert_valid_schema(character, 'character_schema.json')