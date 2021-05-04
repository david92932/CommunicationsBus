from Core.Rule import Rule

class TimeRule(Rule):
    """
    Rule class to validate the processing time is greater than the required time
    """

    def __init__(self, processing_time):

        super().__init__("0")

        self.processingTime = processing_time

    def checkValidValues(self, new_value):
        """
        validate new_value is longer than required processing time
        :param new_value:
        :return:
        """

        rule_violations = []

        if new_value >= self.processingTime:

            pass

        else:
            message = f'Value {new_value} is not long enough.  Would you like to set to {self.processingTime}?'
            rule_violations.append({'Valid': False, 'attemptedValue': self.processingTime, 'overridable': True, 'message': message})

        return rule_violations

    def getTimeLength(self):

        return 0