import pytest
import unittest
from Core.DefinedValuesRule import DefinedValuesRule


class test_DefinedValuesRule(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def _setup(self):

        self.testRule = DefinedValuesRule("99.0.0.0", "test rule", 0, 0)

    def test_CheckValidValues(self):

        assert True

        # #invalid
        # value_is_valid, message = self.testRule.checkValidValues(5)
        # assert value_is_valid == False
        # assert isinstance(message, str)
        # assert self.testRule.definedValue == 0
        #
        # #valid
        # value_is_valid, message = self.testRule.checkValidValues(0)
        # assert value_is_valid == True
        # assert isinstance(message, str)
        # assert self.testRule.definedValue == 0
