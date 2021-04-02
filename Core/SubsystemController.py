from Core.Subsystem import Subsystem
from Core.Command import Command
from Core.CommandFile import CommandFile

import copy

class SubsystemController:

    def __init__(self, subsystem_obj):

        print(f'made subsystemController {subsystem_obj.subsystemName}')

        self.headers: [str] = ['BusEm Id', 'BusEm Start', 'BusEm Length', 'Command Name', 'RT Address',
                        'Sub Address', 'Word Count', 'Enabled']

        self.mySubsystem: Subsystem = subsystem_obj
        self.filePath = None

    def createCommand(self, command_name: str) -> Command:

        new_command = None

        for command in self.mySubsystem.getAllAvailableCommands():
            print(command.name)

        for command in self.mySubsystem.getAllAvailableCommands():

            if command.name == command_name:

                new_command = copy.deepcopy(command)
                self.addCommandAtEnd(new_command)
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

        command_file = CommandFile(self, file_path)
        command_file.writeCommandFile()

    def setFilePath(self, file_path: str):

        if isinstance(file_path, str):
            self.filePath = file_path

    def readCommandFile(self, file_path):
        command_file = CommandFile(self, file_path)
        command_file.readCommandFile()

        for command in self.getSubsystemSchedule():
            print(command.name)

        self.setFilePath(file_path)









