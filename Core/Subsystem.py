from Core.Command import Command

class Subsystem:
    """
    Models a whole Subsystem
    """

    def __init__(self, name: str, file_extension: str, commands: [Command]):
        """
        Loaded from SubsytemParser
        :param name: name of subsystem
        :param file_extension: file extension EX: ccmd
        :param commands: list of Command objs included in Subsystem
        """

        self.subsystemName: str = name
        self.fileExtension: str = file_extension
        self.__commands = commands

        self.__subsystemSchedule = []

        self.timelineRow = 0

    def getSubsystemSchedule(self) -> [Command]:
        """
        Returns whole Subsystem schedule of Commands
        """

        return self.__subsystemSchedule

    def getAllAvailableCommands(self) -> [Command]:
        """
        returns a list of available commands for the Subsystem
        """

        return self.__commands

    def addCommandAtEnd(self, command_obj: Command):
        """
        adds a Command to the end of the Subsystem's schedule
        :param command_obj: Command obj to add
        """

        if isinstance(command_obj, Command):
            self.__subsystemSchedule.append(command_obj)

    def addCommandAtIndex(self, command_obj: Command, index: int):
        """
        insert a command into the schedule at index
        :param command_obj: Command obj to add
        :param index: integer index of location to add
        :return:
        """

        if isinstance(command_obj, Command):

            try:
                self.__subsystemSchedule.insert(index, command_obj)
            except:
                pass

    def removeCommandAtIndex(self, index: int):
        """
        remove a Command at index of schedule
        """

        try:
            del self.__subsystemSchedule[index]
        except:
            pass

    def setTimelineRowAndColor(self, row: int, color: str):
        """
        assigned by ScenarioController the row and color of the timeline
        boxes associated with this Subsystem

        """

        self.timelineRow = row

        for command in self.getAllAvailableCommands():

            command.setTimelineRow(row)
            command.setTimelineColor(color)

    def clearSchedule(self):

        self.__subsystemSchedule = []