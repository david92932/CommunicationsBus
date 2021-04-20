import re

from Core.Rule import Rule

class RegexRule(Rule):

    def __init__(self, version_added: str, regex_expression: str):

        super().__init__(version_added)

        self.regexExpression = re.compile(regex_expression)

    def checkValidValues(self, new_value):

        rule_violations = []
        value_is_valid = re.fullmatch(self.regexExpression, new_value)

        if not value_is_valid:
            message = 'New Entry does not match regex expression'
            rule_violations.append({'Valid': value_is_valid, 'attemptedValue': new_value, 'overridable': False, 'message': message})

        return rule_violations

    def getTimeLength(self):
        return 0