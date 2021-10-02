from fightclub_setup.superhero_api import *

# Using pytest fixtures for common variables

class TestSuperHero:
    # We need to secure that there are not going to be repeted characters
    def test_ids_are_unique(self, random_id_list):
        unique_ids = set(random_id_list)
        assert len(random_id_list) == len(unique_ids)  # there are no repetitions

    def test_ids_are_in_range(self, random_id_list):
        ids_out_of_range = list(
            filter(
                lambda x: x if (x < 1 or x > total_number_of_characters) else None, random_id_list
            )
        )
        assert 0 == len(ids_out_of_range)

    def test_get_random_id(self, random_id):
        assert type(random_id) is int
        assert random_id > 0

    def test_get_single_character_success(self, random_id):
        character = get_character(random_id)
        assert character  # checks character exists
        assert character["response"] == "success"

    def test_get_single_character_fail(self):
        character = get_character(0)
        assert character
        assert character["response"] == "error"

    def test_random_list_of_characters_is_not_empty(self, number_of_ids):
        list_of_characters = get_random_list_of_characters(number_of_ids)
        assert isinstance(list_of_characters, list)
        assert 10 == len(list_of_characters)

    def test_random_list_of_characters_is_empty(self):
        list_of_characters = get_random_list_of_characters(0)
        assert isinstance(list_of_characters, list)
        assert 0 == len(list_of_characters)
