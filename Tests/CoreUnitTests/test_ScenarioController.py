import pytest
import unittest
from Core.SubsystemParser import SubsystemParser
from Core.ScenarioController import ScenarioController

class test_ScenarioController(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def _setup(self):
        file_path = "/Users/David/PycharmProjects/CommunicationsBus/Assets/Camera2.json"
        subsystem_parser = SubsystemParser(file_path)

        self.testSubsystem = subsystem_parser.getSubsystem()
        self.testScenarioController = ScenarioController([self.testSubsystem])

    def test_create_subsystem(self):

        #valid
        subystem_name = self.testSubsystem.subsystemName
        self.testScenarioController.createSubsystem(subystem_name)

        assert self.testScenarioController.getActiveSubsystems()[0].mySubsystem.subsystemName == subystem_name
        assert len(self.testScenarioController.getActiveSubsystems()) == 1

        #invalid
        self.testScenarioController.createSubsystem(None)
        assert len(self.testScenarioController.getActiveSubsystems()) == 1


    def test_remove_subsystem_at_index(self):

        #valid
        self.testScenarioController.removeActiveSubystemAtIndex(0)
        active_subsystems = self.testScenarioController.getActiveSubsystems()
        assert len(active_subsystems) == 0

        #invalid
        self.testScenarioController.removeActiveSubystemAtIndex(5)
        active_subsystems = self.testScenarioController.getActiveSubsystems()
        assert len(active_subsystems) == 0