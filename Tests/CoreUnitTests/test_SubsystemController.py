import pytest
import unittest
from Core.SubsystemParser import SubsystemParser
from Core.SubsystemController import SubsystemController
from Core.Command import Command

class test_SubsystemController(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def _setup(self):

        file_path = "/Users/David/PycharmProjects/CommunicationsBus/Assets/Camera2.json"
        subsystem_parser = SubsystemParser(file_path)

        self.testSubsystem = subsystem_parser.getSubsystem()
        self.testSubsystemController = SubsystemController(self.testSubsystem)

    def test_create_command(self):

        # pass None
        new_command = self.testSubsystemController.createCommand(None)
        assert new_command == None

        # pass valid
        available_command_1 = self.testSubsystemController.getAllAvailableCommands()[0]
        command_name = available_command_1.name

        new_command = self.testSubsystemController.createCommand(command_name)

        assert isinstance(new_command, Command)
        assert new_command.name == command_name

        return new_command

    def test_clear_subystem_schedule(self):

        self.testSubsystemController.clearSubsystemSchedule()
        subsystem_schedule = self.testSubsystemController.getSubsystemSchedule()
        assert len(subsystem_schedule) == 0

    def test_subystem_schedule(self):

        self.test_clear_subystem_schedule()

        new_command = self.test_create_command()

        subsystem_schedule = self.testSubsystemController.getSubsystemSchedule()

        assert len(subsystem_schedule) == 1

    def test_create_at_index(self):

        self.test_clear_subystem_schedule()
        print('clearing subsystem')
        print(self.testSubsystemController.getSubsystemSchedule())
        new_command = self.test_create_command()

        # valid index
        self.testSubsystemController.addCommandAtEnd(new_command)
        self.testSubsystemController.addCommandAtIndex(new_command, 1)
        subsystem_schedule = self.testSubsystemController.getSubsystemSchedule()
        assert subsystem_schedule[1] == new_command

        #invalid index
        self.testSubsystemController.addCommandAtIndex(new_command, 3)
        subsystem_schedule = self.testSubsystemController.getSubsystemSchedule()
        for i in subsystem_schedule:
            print(i.name)
        assert len(subsystem_schedule) == 4

        #invalid command
        self.testSubsystemController.addCommandAtIndex(None, 2)
        assert len(subsystem_schedule) == 4

    def test_create_command_at_end(self):

        self.test_clear_subystem_schedule()
        subsystem_schedule = self.testSubsystemController.getSubsystemSchedule()

        new_command = self.test_create_command()
        self.testSubsystemController.addCommandAtEnd(new_command)

        subsystem_schedule = self.testSubsystemController.getSubsystemSchedule()
        assert(subsystem_schedule[0] == new_command)
        assert(len(subsystem_schedule) == 2)

        self.test_clear_subystem_schedule()
        self.testSubsystemController.addCommandAtEnd(None)
        subsystem_schedule = self.testSubsystemController.getSubsystemSchedule()
        assert(len(subsystem_schedule) == 0)

    def test_remove_command_at_index(self):

        self.test_clear_subystem_schedule()
        new_command = self.test_create_command()

        #valid
        self.testSubsystemController.removeCommandAtIndex(0)
        subsystem_schedule = self.testSubsystemController.getSubsystemSchedule()
        assert len(subsystem_schedule) == 0

        #invalid
        new_command = self.test_create_command()
        self.testSubsystemController.removeCommandAtIndex(5)
        subsystem_schedule = self.testSubsystemController.getSubsystemSchedule()
        assert len(subsystem_schedule) == 1

    def test_set_file_path(self):

        #valid
        test_file_path = '/test/file/path'
        self.testSubsystemController.setFilePath(test_file_path)

        assert self.testSubsystemController.filePath == test_file_path

        #invalid
        self.testSubsystemController.setFilePath(None)
        assert self.testSubsystemController.filePath == test_file_path