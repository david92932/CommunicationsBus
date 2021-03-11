from Core.Subsystem import Subsystem
from Core.Command import Command
from Core.CommandFile import CommandFile

import copy

class SubsystemController:

    def __init__(self, subsystem_name: str, all_subsystem_models: [Subsystem]):

        print(f'made subsystemController {subsystem_name}')

        self.headers: [str] = ['BusEm Id', 'BusEm Start', 'BusEm Length', 'Command Name', 'RT Address',
                        'Sub Address', 'Word Count', 'Enabled']

        self.allSubsystemModels: [Subsystem] = all_subsystem_models

        self.createSubsystem(subsystem_name)

        self.mySubsystem: Subsystem

    def createSubsystem(self, name: str):

        for subsystem in self.allSubsystemModels:

            sub_name = subsystem.subsystemName

            if sub_name == name:

                self.mySubsystem = copy.deepcopy(subsystem)

    def createCommand(self, command_name: str) -> Command:

        new_command = None

        for command in self.mySubsystem.getAllAvailableCommands():
            print(command.name)

        for command in self.mySubsystem.getAllAvailableCommands():

            if command.name == command_name:

                new_command = copy.deepcopy(command)
                self.addCommandAtEnd(new_command)
                break

        if new_command is not None:
            print(f'New Command {command.name}')

        else:
            print('new command is None :(')

        return new_command

    def getSubsystemSchedule(self) -> Subsystem:

        return self.mySubsystem.getSubsystemSchedule()

    def addCommandAtEnd(self, command_obj: Command):

        self.mySubsystem.addCommandAtEnd(command_obj)

    def addCommandAtIndex(self, command_obj: Command, index: int):

        self.mySubsystem.addCommandAtIndex(command_obj, index)

    def removeCommandAtIndex(self, index: int):

        self.mySubsystem.removeCommandAtIndex(index)

    def getAllAvailableCommands(self) -> [Command]:

        return self.mySubsystem.getAllAvailableCommands()

    def buildCommandFile(self, file_path):

        command_file = CommandFile(self, file_path)
        command_file.writeCommandFile()

    def readCommandFile(self, file_path):








