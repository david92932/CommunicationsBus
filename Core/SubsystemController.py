from Core.Subsystem import Subsystem

import copy

class SubsystemController:

    def __init__(self, subsystem_name, all_subsystem_models):

        print(f'made subsystemController {subsystem_name}')

        self.headers = ['BusEm Id', 'BusEm Start', 'BusEm Length', 'Command Name', 'RT Address',
                        'Sub Address', 'Word Count', 'Enabled']

        self.allSubsystemModels = all_subsystem_models

        self.createSubsystem(subsystem_name)

        self.mySubsystem: Subsystem

    def createSubsystem(self, name):

        for subsystem in self.allSubsystemModels:

            sub_name = subsystem.subsystemName

            if sub_name == name:

                self.mySubsystem = copy.deepcopy(subsystem)

    def createCommand(self, command_name):

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

    def getSubsystemSchedule(self):

        return self.mySubsystem.getSubsystemSchedule()

    def addCommandAtEnd(self, command_obj):

        self.mySubsystem.addCommandAtEnd(command_obj)

    def addCommandAtIndex(self, command_obj, index):

        self.mySubsystem.addCommandAtIndex(command_obj, index)

    def removeCommandAtIndex(self, index):

        self.mySubsystem.removeCommandAtIndex(index)

    def getAllAvailableCommands(self):

        return self.mySubsystem.getAllAvailableCommands()





