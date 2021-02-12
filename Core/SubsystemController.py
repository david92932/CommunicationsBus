import copy

class SubsystemController:

    def __init__(self, all_subsystem_models):

        self.allSubsystemModels = all_subsystem_models


        self.allActiveSubsystems = []

    def createSubsystem(self, name):

        for subsystem in self.allSubsystemModels:

            sub_name = subsystem.subsystemName

            if sub_name == name:

                new_subsystem = copy.deepcopy(subsystem)



