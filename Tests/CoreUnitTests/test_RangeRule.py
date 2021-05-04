import pytest
import unittest
from Core.RangeRule import RangeRule


class test_RangeRule(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def _setup(self):

        self.testRule = RangeRule("99.0.0.0", 0, 250, 2, 1)

    def test_CheckValidValues(self):
        testRule = RangeRule("99.0.0.0", 0, 250, 2, 1)

        #invalid min value
        value_is_valid = testRule.checkValidValues(-6)
        assert value_is_valid[0]["Valid"] == False
        assert isinstance(value_is_valid[0]["message"], str)


        #invalid max value
        value_is_valid= testRule.checkValidValues(252)
        assert value_is_valid[0]["Valid"] == False
        assert isinstance(value_is_valid[0]["message"], str)

        #invalid not divisible
        value_is_valid= testRule.checkValidValues(51)
        print(value_is_valid)
        assert value_is_valid == []


        #invalid, too big for field
        value_is_valid= testRule.checkValidValues(3000)
        print(value_is_valid)
        assert value_is_valid[0]["Valid"] == False
        assert isinstance(value_is_valid[0]["message"], str)

        #valid
        value_is_valid= testRule.checkValidValues(100)

        assert value_is_valid == []
