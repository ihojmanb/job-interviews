"""
conftest.py for test_superhero_api
"""
import pytest
from ..conftest import *

@pytest.fixture()
def number_of_ids():
    return int(10)
    
@pytest.fixture(autouse=True)
def random_id(superhero_consumer):
    return superhero_consumer.get_random_id()

@pytest.fixture
def random_id_list(number_of_ids, superhero_consumer):
    return superhero_consumer.get_list_of_ids(number_of_ids)