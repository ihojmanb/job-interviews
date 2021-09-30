import unittest
from superhero_api import *

class SuperHeroTest(unittest.TestCase):

    def test_check_ids_are_unique(self):
        ids = get_list_of_ids()
        unique_ids = set(ids)
        self.assertEqual(len(ids), len(unique_ids))

    def test_check_ids_are_in_range(self):
        ids = get_list_of_ids()
        ids_out_of_range = list(filter(lambda x: x if (x < 1 or x > 731) else None, ids))
        self.assertEqual(0, len(ids_out_of_range))

    def test_get_random_id(self):
        random_id = get_random_id()
        self.assertIsInstance(random_id, int)

    def test_get_single_character(self):
        id = get_random_id()
        character = get_character(id)
        self.assertTrue(character)
        self.assertEqual(character["response"], "success")


    # def test_check_list_of_characters_is_not_empty(self):
    #     list_of_characters = get_list_of_characters(10)
    #     self.assertTrue(list_of_characters)
    #     self.assertEqual(10, len(list_of_characters))



if __name__ == "__main__":
    unittest.main()
