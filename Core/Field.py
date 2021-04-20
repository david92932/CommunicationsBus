from Core.RangeRule import RangeRule
from Core.TimeRule import TimeRule
from Core.DefinedValuesRule import DefinedValuesRule
from Core.TypeConverter import TypeConverter
from Core.RegexRule import RegexRule

class Field:


    def __init__(self, name: str, byte_size: int, field_description: str, field_rules: [], field_units: str, field_affects_time_length):

        self.name = name
        self.byteSize = byte_size
        self.fieldDescription = field_description
        self.fieldRules = field_rules
        self.fieldUnits = field_units
        self.fieldAffectsTimeLength = field_affects_time_length

        self.fieldValue = 0
        self.fieldValueChanged = False
        self.typeConverter = TypeConverter()
        self.valueLSB = None
        self.ownerCommand = None
        self.fieldSigned = self.__determineIfFieldIsSigned()

    def validateFieldValue(self):

        rule_violations = []

        if self.fieldValue is not None:
            rule_violations = self.__validate(self.fieldValue)

        return rule_violations

    def __validate(self, new_value):

        all_violations = []

        for rule in self.fieldRules:

            if isinstance(rule, DefinedValuesRule):

                defined_value_valid = False
                defined_value_violations = []
                for defined_rule in self.fieldRules:

                    value_is_valid_tuple_list = defined_rule.checkValidValues(new_value)

                    #empty list means value is valid
                    if value_is_valid_tuple_list == []:
                        defined_value_valid = True
                        break

                    else:
                        defined_value_violations = value_is_valid_tuple_list

                if not defined_value_valid:
                    all_violations.extend(defined_value_violations)

            else:

                validation_response = rule.checkValidValues(new_value)

                if validation_response != []:

                    all_violations.extend(validation_response)

        return all_violations

    def setFieldValue(self, value, override_rule_check=False) -> (bool, str):

        rule_violations = []
        value_to_set = self.convertToRawValue(value)

        if override_rule_check:

            self.fieldValue = value_to_set

            rule_violations = []

        else:

            rule_violations = self.__validate(value_to_set)

            # if the value is valid, set it
            if rule_violations == []:

                self.fieldValue = value_to_set

            # otherwise, rule is not valid
            else:

                print(rule_violations)

        return {'fieldName': self.name, 'violations': rule_violations, 'fieldObj': self}

    def convertToRawValue(self, value):

        if self.fieldRules == []:
            value_to_set = int(value)

        else:

            for rule in self.fieldRules:

                if isinstance(rule, TimeRule) or isinstance(rule, DefinedValuesRule):

                    value_to_set = int(value)
                    break

                elif isinstance(rule, RegexRule):
                    value_to_set = value

                else:

                    self.valueLSB = rule.lsbValue
                    value_to_set = self.typeConverter.convertEngineeringToRaw(float(value), self.valueLSB)
                    break

        return value_to_set

    def getFieldValueEngineeringUnits(self):

        if self.valueLSB is not None:
            print(self.fieldValue)
            engineering_value = self.typeConverter.convertRawToEngineering(self.fieldValue, self.valueLSB)

        else:
            engineering_value = self.fieldValue

        return engineering_value

    def getFieldValueRawUnits(self):

        return self.fieldValue

    def calculateTimeLength(self):

        total_field_length = 0
        is_not_defined_range_rule = True

        for rule in self.fieldRules:

            if isinstance(rule, DefinedValuesRule):
                if rule.definedValue == self.fieldValue:
                    total_field_length += rule.getTimeLength()
                    is_not_defined_range_rule = False

            else:
                pass

        if is_not_defined_range_rule and self.fieldAffectsTimeLength:
            total_field_length += self.getFieldValueEngineeringUnits()

        return total_field_length

    def __determineIfFieldIsSigned(self):

        field_signed = False

        for rule in self.fieldRules:

            if isinstance(rule, RangeRule):

                if rule.minValue < 0:

                    field_signed = True
                    break

        return field_signed