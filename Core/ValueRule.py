from Rule import Rule

class ValueRule(Rule):

    def __init__(self):

        self.validHigh: hex
        self.validLow: hex
        self.increment: hex