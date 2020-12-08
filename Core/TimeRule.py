from Rule import Rule

class TimeRule(Rule):

    def __init__(self):

        self.minTimeBefore: int
        self.minTimeAfter: int
        self.minCommandTime: int