from abc import abstractmethod


class Rule:

    def __init__(self, version_added: str):

        self.versionAdded: str = version_added

    @abstractmethod
    def __checkValidValues(self, new_value) -> bool:

        pass


