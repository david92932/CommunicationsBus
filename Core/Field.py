from Core.RangeRule import RangeRule
from Core.TimeRule import TimeRule
from Core.DefinedValuesRule import DefinedValuesRule
from Core.TypeConverter import TypeConverter

class Field:


    def __init__(self, name: str, byte_size: int, field_description: str, field_rules: [], field_units: str):

        self.name = name
        self.byteSize = byte_size
        self.fieldDescription = field_description
        self.fieldRules = field_rules
        self.fieldUnits = field_units

        self.fieldValue = 0
        self.fieldValueChanged = False
        self.typeConverter = TypeConverter()
        self.valueLSB = None

    def setFieldValue(self, value, override_rule_check=False) -> (bool, str):

        print(f'setting {self.name}')
        defined_values_rule = False
        value_to_set = 0

        value_is_valid = True
        response_message = 'Value Is Valid'

        if override_rule_check:

            if self.valueLSB is not None:
                self.fieldValue = self.typeConverter.convertEngineeringToRaw(float(value), self.valueLSB)

            else:
                self.fieldValue = int(value)

            return True, "Value Set Successfully"

        else:
            # add rule checks
            define_values_rule_objs = []
            for rule in self.fieldRules:

                if isinstance(rule, DefinedValuesRule):
                    defined_values_rule = True
                    define_values_rule_objs.append(rule)


            # in a defined values rule, only one needs to be valid
            if defined_values_rule:

                field_valid = False

                value_to_set = int(value)

                for rule in self.fieldRules:
                    if isinstance(rule, DefinedValuesRule):

                        value_is_valid, response_message = rule.checkValidValues(value_to_set)
                        if value_is_valid:
                            field_valid = True
                            break

                # if the definedvalues are not valid, stop here and return message
                if not value_is_valid:
                    return False, response_message

            # check every other type of rule
            for rule in self.fieldRules:

                if isinstance(rule, TimeRule):
                    print('Time Rule')
                    value_to_set = int(value)
                    value_is_valid, response_message = rule.checkValidValues(value_to_set)
                    print(f'RESPONSE: {value_is_valid, response_message}')

                elif isinstance(rule, RangeRule):
                    lsb_value_from_rule = rule.lsbValue
                    self.valueLSB = lsb_value_from_rule
                    value_to_set = self.typeConverter.convertEngineeringToRaw(float(value), lsb_value_from_rule)
                    value_is_valid, response_message = rule.checkValidValues(value_to_set)

            if value_is_valid:
                print(f'setting field {self.name} to {value_to_set}')
                self.fieldValue = value_to_set
                self.fieldValueChanged = True

            else:
                print(response_message)

        i = (value_is_valid, response_message)
        print(f'type: {type(i)}')
        print(f'qwe: {i}')

        return i

    def getFieldValueEngineeringUnits(self):

        if self.valueLSB is not None:
            engineering_value = self.typeConverter.convertRawToEngineering(self.fieldValue, self.valueLSB)

        else:
            engineering_value = self.fieldValue

        return engineering_value

    def getFieldValueRawUnits(self):

        return self.fieldValue