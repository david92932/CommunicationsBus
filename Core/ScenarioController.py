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