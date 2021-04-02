from Core.Command import Command

class Subsystem:

    def __init__(self, name: str, file_extension: str, commands: [Command]):

        self.subsystemName: str = name
        self.fileExtension: str = file_extension
        self.__commands = commands

        self.__subsystemSchedule = []

        self.timelineRow = 0

    def getSubsystemSchedule(self) -> [Command]:

        return self.__subsystemSchedule

    def getAllAvailableCommands(self) -> [Command]:

        return self.__commands

    def addCommandAtEnd(self, command_obj: Command):

        if isinstance(command_obj, Command):
            self.__subsystemSchedule.append(command_obj)

    def addCommandAtIndex(self, command_obj: Command, index: int):

        if isinstance(command_obj, Command):

            try:
                self.__subsystemSchedule.insert(index, command_obj)
            except:
                pass

    def removeCommandAtIndex(self, index: int):

        try:
            del self.__subsystemSchedule[index]
        except:
            pass

    def setTimelineRow(self, row: int):

        self.timelineRow = row

        for command in self.getAllAvailableCommands():

            command.setTimelineRow(row)

    def clearSchedule(self):

        self.__subsystemSchedule = []