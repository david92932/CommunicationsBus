

class Field:


    def __init__(self, name: str, byte_size: int, field_description: str, field_rules: [], field_units: str):
                 # min_value, max_value, lsb_value):

        self.name = name
        self.byteSize = byte_size
        self.fieldDescription = field_description
        self.fieldRules = field_rules
        self.fieldUnits = field_units


        self.fieldValue = 0

    def setFieldValue(self, value) -> (bool, str):

        field_value = float(value)

        value_is_valid = True
        response_message = ''

        # # add rule checks
        # for rule in self.fieldRules:
        #
        #     valid_for_rule, message = rule.checkValidValues(field_value)
        #
        #     if valid_for_rule:
        #         value_is_valid = True
        #         response_message = message
        #
        #     elif not valid_for_rule:
        #         value_is_valid = False
        #         response_message = message
        #         break

        if value_is_valid:
            print(f'setting field {self.name} to {field_value}')
            self.fieldValue = field_value
        else:
            print(response_message)

        return value_is_valid, response_message

    def getFieldValueEngineeringUnits(self):

        return self.fieldValue

    def getFieldValueRawUnits(self):

        return self.fieldValue