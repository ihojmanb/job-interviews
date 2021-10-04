"""
conftest.py for test_superhero_api
"""
from fightclub_setup.superhero_api import *
import pytest

@pytest.fixture()
def number_of_ids():
    return int(10)
    
@pytest.fixture(autouse=True)
def random_id():
    return get_random_id()

@pytest.fixture
def random_id_list(number_of_ids):
    return get_list_of_ids(number_of_ids)