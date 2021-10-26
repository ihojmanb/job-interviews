"""
conftest.py for *.py
"""

import pytest
import json
from stocks.stocks import *

@pytest.fixture
def credentials():
    credentials = open("credentials.json")
    credentials = json.load(credentials)
    return credentials