from Core.Command import Command

class Subsystem:

    def __init__(self, name: str, file_extension: str, commands: [Command]):

        self.subsystemName = name
        self.__fileExtension = file_extension
        self.__commands = commands

        self.__subsystemSchedule = []

    def getSubsystemSchedule(self):

        return self.__subsystemSchedule

    def getAllAvailableCommands(self):

        return self.__commands

    def addCommandAtEnd(self, command_obj):

        self.__subsystemSchedule.append(command_obj)

    def addCommandAtIndex(self, command_obj, index):

        self.__subsystemSchedule.insert(index, command_obj)

    def removeCommandAtIndex(self, index):

        del self.__subsystemSchedule[index]