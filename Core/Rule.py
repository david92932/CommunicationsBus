from abc import abstractmethod


class Rule:
    """
    Abstract Rule class implementation. All Rule classes
    inherit from Rule and are required to include several functions
    """

    def __init__(self, version_added: str):

        self.versionAdded: str = version_added

    @abstractmethod
    def checkValidValues(self, new_value):
        """
        See other rule class for more specific implementation

        This function is to check that new_value is valid for that Rule
        """

        pass

    @abstractmethod
    def getTimeLength(self):
        """
        Calculate processing time required for specific field values
        only implemented in DefinedValuesRule
        :return:
        """
        pass


