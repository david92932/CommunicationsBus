import copy
from Core.SubsystemController import SubsystemController

class ScenarioController:
    """
    the ScenarioController controls 1 scenario
    It is assumed that all open files are part of 1 scenario
    """

    # color to assign to different timeline rows (doesn't work)
    TIMELINE_COLORS = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow']

    def __init__(self, all_subsystem_models):

        self.subsystemModels = all_subsystem_models
        self.activeSubsystems = []


    def createSubsystem(self, name: str):
        """
        Create a SubsystemController object from the name of the
        subsystem
        :param name: name of subsystem to create (must be loaded from startUp)
        EX: 'Recorder'
        :return: SubsystemController obj that is implemented with Subsystem
        of name
        """

        subsystem_controller = None

        for subsystem in self.subsystemModels:

            sub_name = subsystem.subsystemName

            if sub_name == name:

                new_subsystem = copy.deepcopy(subsystem)
                subsystem_controller = SubsystemController(new_subsystem)
                self.activeSubsystems.append(subsystem_controller)

                index = self.activeSubsystems.index(subsystem_controller)
                color = ScenarioController.TIMELINE_COLORS[index]
                new_subsystem.setTimelineRowAndColor(index, color)

                break

        return subsystem_controller

    def getAvailableSubsystemNames(self):
        """
        get a list of strings for all subsystems that are available to the users
        :return: list of strings EX: ['Camera', 'Recorder']
        """

        subsystems_list = []

        for subsystem in self.subsystemModels:

            subsystems_list.append(subsystem.subsystemName)

        return subsystems_list

    def getActiveSubsystems(self):

        return self.activeSubsystems

    def getSubsystemFromFileExtension(self, file_extension: str):
        """
        create a Subsystem from a file_extension
        :param file_extension: file extension to find EX: .ccmd
        :return: SubystemController obj with new Subsystem
        """

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
        """
        remove SubsystemController at index of self.activeSubsystems
        :param index: integer index
        :return: N/A
        """

        try:
            self.activeSubsystems.pop(index)
        except:
            pass

    def writeScenarioFile(self, scenario_file_path: str):
        """
        Writes a scenario file with including all subsystems that are currently open
        :param scenario_file_path: file path to write Scenario file
        :return: N/A
        """

        with open(scenario_file_path, 'a') as outFile:
            for subsystem_controller in self.getActiveSubsystems():
                subsystem_file_path = subsystem_controller.filePath
                outFile.write(f'{subsystem_file_path}\n')

        outFile.close()

    def openScenarioFile(self, scenario_file_path: str):
        """
        Open a Sceanario file and load all subsystems included into the application
        :param scenario_file_path: file path to read scenario file from
        """

        with open(scenario_file_path, 'r') as inFile:
            command_file_paths = inFile.readlines()
        inFile.close()

        for command_file_path in command_file_paths:

            command_file_path = command_file_path.strip('\n')
            file_extension = command_file_path.split('.')[1]

            new_subsystem_controller = self.getSubsystemFromFileExtension(file_extension)
            new_subsystem_controller.readCommandFile(command_file_path)