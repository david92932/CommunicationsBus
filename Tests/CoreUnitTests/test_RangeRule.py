import pytest
import unittest
from Core.RangeRule import RangeRule


class test_RangeRule(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def _setup(self):

        self.testRule = RangeRule("99.0.0.0", 0, 250, 2, 1)

    def test_CheckValidValues(self):

        #invalid min value
        value_is_valid, message = self.testRule.checkValidValues(-6)
        assert value_is_valid == False
        assert isinstance(message, str)

        #invalid max value
        value_is_valid, message = self.testRule.checkValidValues(252)
        assert value_is_valid == False
        assert isinstance(message, str)

        #invalid not divisible
        value_is_valid, message = self.testRule.checkValidValues(51)
        assert value_is_valid == False
        assert isinstance(message, str)

        #invalid, too big for field
        value_is_valid, message = self.testRule.checkValidValues(3000)
        assert value_is_valid == False
        assert isinstance(message, str)

        #valid
        value_is_valid, message = self.testRule.checkValidValues(100)
        print(message)
        assert value_is_valid == True
