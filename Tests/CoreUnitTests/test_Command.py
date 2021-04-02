import pytest
import unittest
from Core.Command import Command
from Core.Field import Field
from Core.SubsystemParser import SubsystemParser
from Core.ScenarioController import ScenarioController

class test_Command(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def _setup(self):
        file_path = "/Users/David/PycharmProjects/CommunicationsBus/Assets/Camera.json"
        subsystem_parser = SubsystemParser(file_path)

        testSubsystem = subsystem_parser.getSubsystem()
        self.testCommand = testSubsystem.getAllAvailableCommands()[0]

    def test_command_fields(self):

        command_fields = self.testCommand.getCommandFields()

        for field in command_fields:
            assert isinstance(field, Field)