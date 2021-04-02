import copy
from Core.SubsystemController import SubsystemController

class ScenarioController:

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
                new_subsystem.setTimelineRow(self.activeSubsystems.index(subsystem_controller))

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

        subsystem_name = None
        for subsystem in self.subsystemModels:

            subsystem_extension = subsystem.fileExtension

            if subsystem_extension == file_extension:
                subsystem_name = subsystem.subsystemName
                break

        if subsystem_name is not None:
            new_subsystem_controller = self.createSubsystem(subsystem_name)

        return new_subsystem_controller

    def removeActiveSubystemAtIndex(self, index: int):

        try:
            self.activeSubsystems.pop(index)
        except:
            pass

    def writeScenarioFile(self, scenario_file_path: str):

        with open(scenario_file_path, 'w') as outFile:
            for subsystem_controller in self.getActiveSubsystems():
                subsystem_file_path = subsystem_controller.filePath
            outFile.write(f'{subsystem_file_path}\n')

        outFile.close()

    def openScenarioFile(self, scenario_file_path: str):

        with open(scenario_file_path, 'r') as inFile:
            command_file_paths = inFile.readlines()
        inFile.close()

        for command_file_path in command_file_paths:

            file_extension = command_file_path.split('.')[1]
            new_subsystem_controller = self.getSubsystemFromFileExtension(file_extension)
            new_subsystem_controller.readCommandFile(command_file_path)