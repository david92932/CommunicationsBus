from Core.RangeRule import RangeRule
from Core.TimeRule import TimeRule
from Core.DefinedValuesRule import DefinedValuesRule

class Field:


    def __init__(self, name: str, byte_size: int, field_description: str, field_rules: [], field_units: str):

        self.name = name
        self.byteSize = byte_size
        self.fieldDescription = field_description
        self.fieldRules = field_rules
        self.fieldUnits = field_units

        self.fieldValue = 0
        self.fieldValueChanged = False

    def setFieldValue(self, value) -> (bool, str):

        defined_values_rule = False
        field_value = float(value)

        value_is_valid = True
        response_message = ''

        # # add rule checks
        # define_values_rule_objs = []
        # for rule in self.fieldRules:
        #
        #     if isinstance(rule, DefinedValuesRule):
        #         defined_values_rule = True
        #         define_values_rule_objs.append(rule)
        #
        #
        # # in a defined values rule, only one needs to be valid
        # if defined_values_rule:
        #
        #     field_valid = False
        #
        #     for rule in self.fieldRules:
        #         if isinstance(rule, DefinedValuesRule):
        #
        #             value_is_valid, response_message = rule.checkValidValues(value)
        #             if value_is_valid:
        #                 field_valid = True
        #                 break
        #
        #     # if the definedvalues are not valid, stop here and return message
        #     if not value_is_valid:
        #         return False, response_message
        #
        # # check every other type of rule
        # for rule in self.fieldRules:
        #
        #     if isinstance(rule, TimeRule):
        #         value_is_valid, response_message = rule.checkValidValues(value)
        #
        #     elif isinstance(rule, RangeRule):
        #         value_is_valid, response_message = rule.checkValidValues(value)

        if value_is_valid:
            print(f'setting field {self.name} to {field_value}')
            self.fieldValue = field_value
            self.fieldValueChanged = True

        else:
            print(response_message)

        return value_is_valid, response_message

    def getFieldValueEngineeringUnits(self):

        return self.fieldValue

    def getFieldValueRawUnits(self):

        return self.fieldValue