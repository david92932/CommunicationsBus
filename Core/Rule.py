from abc import abstractmethod


class Rule:

    def __init__(self, version_added: str):

        self.versionAdded: str = version_added

    @abstractmethod
    def checkValidValues(self, new_value):

        pass

    @abstractmethod
    def getTimeLength(self):
        pass


