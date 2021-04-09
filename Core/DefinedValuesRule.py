from Core.Rule import Rule


class DefinedValuesRule(Rule):

    def __init__(self, version_added: str, name: str, value, processing_time):
        super().__init__(version_added)

        self.name = name
        self.definedValue = value
        self.processingTime = processing_time

    def checkValidValues(self, new_value):
        value_is_valid = False

        if self.definedValue == new_value:
            value_is_valid = True

        if value_is_valid:
            return (True, "Value is valid")

        else:
            return (False, f"Value {new_value} is not valid")

    def getTimeLength(self):

        if self.processingTime is not None:
            return self.processingTime

        else:
            return 0