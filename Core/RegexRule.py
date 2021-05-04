import re

from Core.Rule import Rule

class RegexRule(Rule):
    """
    A RegexRule is a rule for a string Field where the entry must match a
    regex expression
    """

    def __init__(self, version_added: str, regex_expression: str):

        super().__init__(version_added)

        self.regexExpression = re.compile(regex_expression)

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
        value_is_valid = re.fullmatch(self.regexExpression, new_value)

        if not value_is_valid:
            message = 'New Entry does not match regex expression'
            rule_violations.append({'Valid': value_is_valid, 'attemptedValue': new_value, 'overridable': False, 'message': message})

        return rule_violations

    def getTimeLength(self):
        """
        required by Rule abstract class, but regex rules don't affect time
        :return: 0
        """
        return 0