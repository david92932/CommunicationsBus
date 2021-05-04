from Core.Subsystem import Subsystem
from Core.Command import Command
from Core.CommandFile import CommandFile

import copy

class SubsystemController:
    """
    Responsible for controlling a single Subsystem and adding functionality
    to it
    """

    def __init__(self, subsystem_obj):

        # list of table headers to show on the GUI table
        self.headers: [str] = ['BusEm Id', 'BusEm Start', 'BusEm Length', 'Command Name', 'RT Address',
                        'Sub Address', 'Word Count', 'Enabled']

        self.mySubsystem: Subsystem = subsystem_obj
        self.filePath = None

    def createCommand(self, command_name: str) -> Command:
        """
        Create a Command object from name
        :param command_name: name of command to add to schedule EX 'mode'
        :return: created Command obj that has been added to end of schedule
        """

        new_command = None

        for command in self.mySubsystem.getAllAvailableCommands():

            if command.name == command_name:

                new_command = copy.deepcopy(command)
                self.addCommandAtEnd(new_command)
                break

        return new_command

    def createCommandWithoutAdding(self, command_name: str):
        """
        create a Command obj from command_name, but don't add to schedule
        :return: Command obj created
        """

        new_command = None
        for command in self.mySubsystem.getAllAvailableCommands():

            if command.name == command_name:

                new_command = copy.deepcopy(command)
                break

        return new_command

    def getSubsystemSchedule(self):

        return self.mySubsystem.getSubsystemSchedule()

    def addCommandAtEnd(self, command_obj: Command):

        self.mySubsystem.addCommandAtEnd(command_obj)

    def addCommandAtIndex(self, command_obj: Command, index: int):

        self.mySubsystem.addCommandAtIndex(command_obj, index)

    def removeCommandAtIndex(self, index: int):

        self.mySubsystem.removeCommandAtIndex(index)

    def clearSubsystemSchedule(self):

        self.mySubsystem.clearSchedule()

    def getAllAvailableCommands(self) -> [Command]:

        return self.mySubsystem.getAllAvailableCommands()

    def buildCommandFile(self, file_path):
        """
        Writes command file for Subsystem to file_path
        :param file_path: string file_path to write command file
        :return: N/A
        """

        command_file = CommandFile(self, file_path)
        command_file.writeCommandFile()

    def setFilePath(self, file_path: str):
        """
        set the file path associated with SubsystemSchedule
        (used for saving existing files)
        :param file_path: string file_path to write command file
        """

        if isinstance(file_path, str):
            self.filePath = file_path

    def readCommandFile(self, file_path):
        """
        read command file at file_path and load into Subsystem
        """
        command_file = CommandFile(self, file_path)
        command_file.readCommandFile()

        for command in self.getSubsystemSchedule():
            command.setTimelineBox()

        self.setFilePath(file_path)













