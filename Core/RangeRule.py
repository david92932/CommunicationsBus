from Core.Rule import Rule

class RangeRule(Rule):

    def __init__(self, version_added, min_value, max_value, lsb_value):

        super().__init__(version_added)

        self.minValue = min_value
        self.maxValue = max_value
        self.lsbValue = lsb_value

    def __checkValidValues(self, new_value):

        value_is_valid = False

        min_valid, min_message = self.__checkMinValue(new_value)
        max_valid, max_message = self.__checkMaxValue(new_value)
        lsb_valid, lsb_message = self.__checkDivisible(new_value)

        if not min_valid:
            return min_valid, min_message

        if not max_valid:
            return max_valid, max_message

        if not lsb_valid:
            return lsb_valid, lsb_message

        return (True, "Value Is Valid")

    def __checkMaxValue(self, new_value):

        value_is_valid = False

        # if new value bigger than allowed max value
        if new_value > self.maxValue:

            return(value_is_valid, f"New value {new_value} is larger than max value {self.maxValue}")

        # else
        else:
            value_is_valid = True
            return(value_is_valid, f"Value is valid")

    def __checkMinValue(self, new_value):

        value_is_valid = False

        # if new value smaller than allowed min value
        if new_value < self.minValue:

            return (value_is_valid, f"New value {new_value} is less than min value {self.minValue}")

        # else
        else:
            value_is_valid = True
            return (value_is_valid, f"Value is valid")

    def __checkDivisible(self, new_value):

        value_is_valid = False

        lsb_division_value = new_value / self.lsbValue

        # if new value not divisible (as int) by lsb
        if not isinstance(lsb_division_value, int):

            return (value_is_valid, f"New value {new_value} is not divisible into LSB increment {self.lsbValue}")

        # else
        else:
            value_is_valid = True
            return (value_is_valid, f"Value is valid")