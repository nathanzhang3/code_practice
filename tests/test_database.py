from unittest import TestCase
import pytest

import sys
sys.path.append('.')

import market

@pytest.mark.test_units
class TestDatabase(TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    @pytest.mark.test_database
    def test_initialize_trade_csv(self):
        pass
