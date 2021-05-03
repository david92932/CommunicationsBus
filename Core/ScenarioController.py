import copy
from Core.SubsystemController import SubsystemController

class ScenarioController:

    TIMELINE_COLORS = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow']

    def __init__(self, all_subsystem_models):

        self.subsystemModels = all_subsystem_models
        self.activeSubsystems = []

    def createSubsystem(self, name: str):

        subsystem_controller = None

        for subsystem in self.subsystemModels:

            sub_name = subsystem.subsystemName

            if sub_name == name:

                new_subsystem = copy.deepcopy(subsystem)
                subsystem_controller = SubsystemController(new_subsystem)
                self.activeSubsystems.append(subsystem_controller)

                index = self.activeSubsystems.index(subsystem_controller)
                color = ScenarioController.TIMELINE_COLORS[index]
                print(f'COLOR----------------------{color}')
                new_subsystem.setTimelineRowAndColor(index, color)

                break

        return subsystem_controller

    def getAvailableSubsystemNames(self):

        subsystems_list = []

        for subsystem in self.subsystemModels:

            subsystems_list.append(subsystem.subsystemName)

        return subsystems_list

    def getActiveSubsystems(self):

        return self.activeSubsystems

    def getSubsystemFromFileExtension(self, file_extension: str):

        print(f'function file extension: {file_extension}')

        subsystem_name = None
        for subsystem in self.subsystemModels:

            subsystem_extension = subsystem.fileExtension

            print(f'looking at {subsystem_extension}')

            if subsystem_extension == file_extension:
                subsystem_name = subsystem.subsystemName
                print('found')
                break

        print(subsystem_name)
        if subsystem_name is not None:
            new_subsystem_controller = self.createSubsystem(subsystem_name)

        return new_subsystem_controller

    def removeActiveSubystemAtIndex(self, index: int):

        try:
            self.activeSubsystems.pop(index)
        except:
            pass

    def writeScenarioFile(self, scenario_file_path: str):

        print(self.getActiveSubsystems())
        with open(scenario_file_path, 'a') as outFile:
            for subsystem_controller in self.getActiveSubsystems():
                subsystem_file_path = subsystem_controller.filePath
            outFile.write(f'{subsystem_file_path}\n')

        outFile.close()

    def openScenarioFile(self, scenario_file_path: str):

        with open(scenario_file_path, 'r') as inFile:
            command_file_paths = inFile.readlines()
        inFile.close()

        print(command_file_paths)

        for command_file_path in command_file_paths:

            command_file_path = command_file_path.strip('\n')
            file_extension = command_file_path.split('.')[1]
            print(f'file extension: {file_extension}')
            new_subsystem_controller = self.getSubsystemFromFileExtension(file_extension)
            new_subsystem_controller.readCommandFile(command_file_path)