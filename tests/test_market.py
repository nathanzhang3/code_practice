from unittest import TestCase
import pytest

import sys
sys.path.append('.')

import market

@pytest.mark.test_units
class TestMarket(TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    @pytest.mark.test_market
    def test_initialize_api(self):
        pass
