from Core.SubsystemController import SubsystemController

class ApplicationController:

    def __init__(self, all_subystems):

        self.allSubsystems = all_subystems
        self.subsystemController = SubsystemController(self.allSubsystems)
