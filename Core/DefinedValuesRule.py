from Core.Rule import Rule


class DefinedValuesRule(Rule):
    """
    A DefinedValueRule is a Rule where a field can only be a pre-defined list of values
    """

    def __init__(self, version_added: str, name: str, value, processing_time):
        """

        :param version_added: version Rule was added
        :param name: name of single valid value
        :param value: numerical value associated with that value
        (will get written to output file)
        :param processing_time: additional processing time required if this option is selected
        """
        super().__init__(version_added)

        self.name = name
        self.definedValue = value
        self.processingTime = processing_time

    def checkValidValues(self, new_value):
        """
        Check if new_value is valid according to this rule
        :param new_value: value attempting to set to Field
        :return: rule_violations list with dicts of form
        {'Valid': value_is_valid, 'attemptedValue': new_value, 'overridable': False, 'message': message}
        if a rule has been violated.
        If the rule is valid, rule_violations will be empty
        """
        rule_violations = []
        value_is_valid = False

        if self.definedValue == new_value:
            value_is_valid = True

        if value_is_valid:
            message = 'value is valid'


        else:
            message = f"Value {new_value} is not valid"

            rule_violations.append({'Valid': value_is_valid, 'attemptedValue': new_value, 'overridable': False, 'message': message})

        return rule_violations

    def getTimeLength(self):
        """
        Command processing Time required by this Rule
        """

        if self.processingTime is not None:
            return self.processingTime

        else:
            return 0