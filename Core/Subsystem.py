from Core.Command import Command

class Subsystem:

    def __init__(self, name: str, file_extension: str, commands: [Command]):

        self.subsystemName: str = name
        self.__fileExtension: str = file_extension
        self.__commands: Command = commands

        self.__subsystemSchedule = []

    def getSubsystemSchedule(self) -> [Command]:

        return self.__subsystemSchedule

    def getAllAvailableCommands(self) -> [Command]:

        return self.__commands

    def addCommandAtEnd(self, command_obj: Command):

        self.__subsystemSchedule.append(command_obj)

    def addCommandAtIndex(self, command_obj: Command, index: int):

        self.__subsystemSchedule.insert(index, command_obj)

    def removeCommandAtIndex(self, index: int):

        del self.__subsystemSchedule[index]