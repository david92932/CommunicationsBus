import pytest
import unittest
from Core.Field import Field
from Core.SubsystemParser import SubsystemParser

class test_Field(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def _setup(self):
        file_path = "/Users/David/PycharmProjects/CommunicationsBus/Assets/Camera2.json"
        subsystem_parser = SubsystemParser(file_path)

        testSubsystem = subsystem_parser.getSubsystem()
        testCommand = testSubsystem.getAllAvailableCommands()[0]
        self.testField = testCommand.getCommandFields()[0]

    def test_set_field_value(self):
        file_path = "/Users/Garrett/PycharmProjects/CommunicationsBusApril/Assets/Camera2.json"
        subsystem_parser = SubsystemParser(file_path)

        testSubsystem = subsystem_parser.getSubsystem()
        testCommand = testSubsystem.getAllAvailableCommands()[0]
        testField = testCommand.getCommandFields()[0]

        # valid
        isValid = testField.validateFieldValue()
        print( isValid)
        assert isValid == []



        testSubsystem = subsystem_parser.getSubsystem()
        testCommand = testSubsystem.getAllAvailableCommands()[3]
        testField = testCommand.getCommandFields()[1]

        # invalid State out of range
        isValid = testField.setFieldValue(232322323)
        print("valid",isValid)
        assert isValid["violations"][0]["Valid"] == False