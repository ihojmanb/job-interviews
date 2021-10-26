"""
conftest.py for *.py
"""

import pytest
import json
from stocks_api.stocks_api import *

@pytest.fixture
def credentials():
    credentials = open("credentials.json")
    credentials = json.load(credentials)
    return credentials