from Core.Rule import Rule


class DefinedValuesRule(Rule):

    def __init__(self, version_added: str, name: str, value):
        super().__init__(version_added)

        self.name = name
        self.definedValue = value

    def __checkValidValues(self, new_value):
        value_is_valid = False

        if self.definedValue == new_value:
            value_is_valid = True

        if value_is_valid:
            return (True, "Value is valid")

        else:
            return (False, f"Value {new_value} is not valid")