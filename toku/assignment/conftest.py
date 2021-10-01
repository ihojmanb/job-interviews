"""
conftest.py
"""
from _pytest import python
import pytest

@pytest.fixture
def number_of_characters():
    return 731