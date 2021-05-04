import pytest
import unittest
from Core.DefinedValuesRule import DefinedValuesRule


class test_DefinedValuesRule(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def _setup(self):

        self.testRule = DefinedValuesRule("99.0.0.0", "test rule", 0, 0)

    def test_CheckValidValues(self):
        testRule = DefinedValuesRule("99.0.0.0", "test rule", 0, 0)

        assert True

        #invalid
        value_is_valid= testRule.checkValidValues(5)
        print(value_is_valid)
        assert value_is_valid[0]["Valid"] == False
        assert isinstance(value_is_valid[0]["message"], str)
        assert testRule.definedValue == 0

        #valid
        value_is_valid= testRule.checkValidValues(0)
        assert value_is_valid == []
        assert testRule.definedValue == 0
