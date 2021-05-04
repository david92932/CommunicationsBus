from Core.Rule import Rule
from Core.TypeConverter import TypeConverter

class RangeRule(Rule):
    """
    a RangeRule is a rule where the Field value must be within a specific range of values
    EX: field must be between 1 and 10 and LSB is 1
    so
    min=1
    max=10
    lsb=1
    byte_size=1
    """

    def __init__(self, version_added: str, min_value, max_value, lsb_value, byte_size):

        super().__init__(version_added)

        self.minValue = min_value
        self.maxValue = max_value
        self.lsbValue = lsb_value
        self.byteSize = byte_size
        self.typeConverter = TypeConverter()

    def checkValidValues(self, new_value):
        """
          Check if new_value is valid according to this rule
          :param new_value: value attempting to set to Field
          :return: rule_violations list with dicts of form
          {'Valid': value_is_valid, 'attemptedValue': new_value, 'overridable': False, 'message': message}
          if a rule has been violated.
          If the rule is valid, rule_violations will be empty
          """

        value_is_valid = False

        rule_violations = []

        min_dict = self.__checkMinValue(new_value)
        max_dict = self.__checkMaxValue(new_value)
        lsb_dict = self.__checkDivisible(new_value)
        ff_dict = self.__checkValueFitsInField(new_value)

        ff_value = ff_dict.get('Valid', False)
        if not ff_value:
            rule_violations.append(ff_dict)

        if not min_dict.get('Valid', False):
            rule_violations.append(min_dict)

        if not max_dict.get('Valid', False) and ff_value:
            rule_violations.append(max_dict)

        if not lsb_dict.get('Valid', False):
            rule_violations.append(lsb_dict)

        return rule_violations

    def __checkMaxValue(self, new_value):
        """
        check if new_value is over the allowed max
        """

        value_is_valid = False
        engineering_value = self.typeConverter.convertRawToEngineering(new_value, self.lsbValue)

        # if new value bigger than allowed max value
        if new_value > self.typeConverter.convertEngineeringToRaw(self.maxValue, self.lsbValue):
        # if new_value > self.maxValue:
            value_is_valid = False
            message = f"Field Name: New value " \
                      f"{engineering_value}" \
                      f" is larger than max value {self.maxValue}.  " \
                      f"Would you like set it anyway?"

        # else
        else:
            value_is_valid = True
            message = "Value is Valid"

        return {'Valid': value_is_valid, 'attemptedValue': engineering_value, 'overridable': True, 'message': message}

    def __checkMinValue(self, new_value):
        """
        check if new_value is under the allowed min
        """

        value_is_valid = False

        engineering_value = self.typeConverter.convertRawToEngineering(new_value, self.lsbValue)

        # if new value smaller than allowed min value
        if new_value < self.typeConverter.convertEngineeringToRaw(self.minValue, self.lsbValue):
        # if new_value < self.minValue:
            value_is_valid = False
            message = f"New value {engineering_value} " \
                      f"is less than min value {self.minValue}. Would you like to" \
                      f"set it anyway?"

        # else
        else:
            value_is_valid = True
            message = 'Value Is Valid'

        return {'Valid': value_is_valid, 'attemptedValue': engineering_value, 'overridable': True, 'message': message}

    def __checkDivisible(self, new_value):
        """
        check if new_value is divisible by LSB
        Note: if new_value is not divisisble, dict response
        'attemptedValue': will be a valid value rounded
        to nearest value divisible by the LSB
        """

        value_is_valid = False
        roundedValue = 0.00

        engineering_value = self.typeConverter.convertRawToEngineering(new_value, self.lsbValue)

        lsb_division_value = self.typeConverter.convertRawToEngineering(new_value, self.lsbValue) % self.lsbValue
        #new_value % self.lsbValue

        # if new value not divisible (as int) by lsb
        if not lsb_division_value == 0:

            roundedValue = float(self.lsbValue * round(engineering_value / self.lsbValue))
            value_is_valid = False
            message = f"New value {engineering_value} " \
                      f"is not divisible into LSB increment {self.lsbValue}.  Would you" \
                      f"like to round to {roundedValue}?"

        # else
        else:
            value_is_valid = True
            message = f"Value is valid"

        return {'Valid': value_is_valid, 'attemptedValue': roundedValue, 'overridable': True, 'message': message}

    def __checkValueFitsInField(self, new_value):
        """
        check if new_value fits in the allotted space
        a value can be over the max, but still fit in the
        field, so this function checks if the new_value fits
        in the field

        if this check fails, the value is not overridable because
        it's too big and will throw errors once converted into file
        """

        value_is_valid = False

        number_of_bits = self.byteSize * 8
        max_allowed_value_in_space = pow(2, number_of_bits)

        # if new value not divisible (as int) by lsb
        if max_allowed_value_in_space < new_value:

            value_is_valid = False
            message = f"New value {new_value} does not fit in field of size {self.byteSize}.  Max value" \
                      f"is {max_allowed_value_in_space}"

        # else
        else:
            value_is_valid = True
            message = "Value Is Valid"

        return {'Valid': value_is_valid, 'attemptedValue': new_value, 'overridable': False, 'message': message}

    def getTimeLength(self):

        return 0