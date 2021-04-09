from Core.Rule import Rule

class TimeRule(Rule):

    def __init__(self, processing_time):

        super().__init__("0")

        self.processingTime = processing_time

    def checkValidValues(self, new_value):

       if new_value >= self.processingTime:
           return (True, "Value is Valid")

       else:
           return (False, f"{new_value} is not long enough - must be {self.processingTime}")

    def getTimeLength(self):

        return 0