import pytest
import unittest
from Core.Field import Field
from Core.SubsystemParser import SubsystemParser

class test_Field(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def _setup(self):
        file_path = "/Users/David/PycharmProjects/CommunicationsBus/Assets/Camera.json"
        subsystem_parser = SubsystemParser(file_path)

        testSubsystem = subsystem_parser.getSubsystem()
        testCommand = testSubsystem.getAllAvailableCommands()[0]
        self.testField = testCommand.getCommandFields()[0]

    def test_set_field_value(self):

        self.testField.setFieldValue()