from fightclub_setup.superhero_api import *


class TestSuperHero:
    # We need to secure that there are not going to be repeted characters
    def test_check_ids_are_unique(self):
        ids = get_list_of_ids(10)
        unique_ids = set(ids) 
        assert len(ids) == len(unique_ids) # there are no repetitions

    def test_check_ids_are_in_range(self):
        ids = get_list_of_ids(10)
        ids_out_of_range = list(
            filter(
                lambda x: x if (x < 1 or x > total_number_of_characters) else None, ids
            )
        )
        assert 0 == len(ids_out_of_range)

    def test_get_random_id(self):
        random_id = get_random_id()
        assert type(random_id) is int
        assert random_id > 0

    def test_get_single_character(self):
        id = get_random_id()
        character = get_character(id)
        assert character  # checks character exists
        assert character["response"] == "success"

    def test_check_random_list_of_characters_is_not_empty(self):
        list_of_characters = get_random_list_of_characters(10)
        assert list_of_characters
        assert 10 == len(list_of_characters)
