from Core.RangeRule import RangeRule
from Core.DefinedValuesRule import DefinedValuesRule
from Core.TimeRule import TimeRule
from Core.Command import Command
from Core.Field import Field
from Core.Subsystem import Subsystem

import json

class SubsystemParser:

    def __init__(self, file_path):

        self.path = file_path
        file_json = self.__readFile()

        self.__parseJSON(file_json)

        self.subsystemObject: Subsystem

    def getSubsystem(self):

        return self.subsystemObject

    def __readFile(self) -> dict:

        with open(self.path, "r") as inFile:

            config_json = json.load(inFile)

        return config_json

    def __parseJSON(self, config_json):

        subsystem_name = self.__getDictField(config_json, "subsystemName")
        file_extension = self.__getDictField(config_json, "fileExtension")
        subystem_commands = self.__getDictField(config_json, "commands")

        all_command_objects = self.__parseCommands(subystem_commands)

        self.subsystemObject = Subsystem(subsystem_name, file_extension, all_command_objects)

    def __getDictField(self, json_dict, field_name):

        field_value = json_dict.get(field_name, None)

        if field_value is None:

            raise Exception(f'Error occurred while collecting {field_name} Please Verify in Config File')

        return field_value

    def __parseCommands(self, all_subsystem_commands):

        all_command_objects = []

        for command in all_subsystem_commands:

            command_name = self.__getDictField(command, "name")
            command_id = self.__getDictField(command, "id")
            command_length = self.__getDictField(command, "processingTime")
            rt_address = self.__getDictField(command, "RTAddress")
            sub_address = self.__getDictField(command, "subAddress")
            word_size_in_bits = self.__getDictField(command, "wordSizeInBits")
            command_protocol = self.__getDictField(command, "protocol")
            command_fields = self.__getDictField(command, "fields")
            command_field_objects = self.__parseFields(command_fields)
            command_start_field, command_length_field = self.__parseTimeField(command_length)

            command_obj = Command(command_name, command_id, command_start_field, command_length_field, rt_address, sub_address,
                                  word_size_in_bits, command_protocol, command_field_objects)
            all_command_objects.append(command_obj)

        return all_command_objects

    def __parseTimeField(self, command_length):

        time_rule = TimeRule(command_length)

        time_start_field = Field("Time Start", 64, "Time To Start Command", [], 'ms')
        time_length_field = Field("Time Length", 64, "Duration of Command", [time_rule], 'ms')

        return time_start_field, time_length_field

    def __parseFields(self, all_command_fields):

        all_command_fields_objs = []

        for field in all_command_fields:

            field_name = self.__getDictField(field, "name")
            field_byte_size = self.__getDictField(field, "size")
            field_description = self.__getDictField(field, "description")
            field_valid_values = self.__getDictField(field, "validValues")
            field_units = field.get('Units', 'None')
            field_rules = self.__parseFieldRules(field_valid_values, field_byte_size)

            field_obj = Field(field_name, field_byte_size, field_description, field_rules, field_units)

            all_command_fields_objs.append(field_obj)

        return all_command_fields_objs

    def __parseFieldRules(self, field_valid_values, field_byte_size):

        all_rules = []

        # if valid values are explictly defined
        if "defined" in field_valid_values.keys():

            defined_value_values = field_valid_values.get('defined', [])

            for defined_value in defined_value_values:

                defined_value_name = self.__getDictField(defined_value, 'name')
                defined_value_value = self.__getDictField(defined_value, 'value')

                defined_value_rule_obj = DefinedValuesRule('0.0.0.0', defined_value_name, defined_value_value)
                all_rules.append(defined_value_rule_obj)

        # if valid values are in a range
        elif "min" in field_valid_values.keys() and "max" in field_valid_values.keys() and "lsb" in field_valid_values.keys():

            min_value = float(self.__getDictField(field_valid_values, 'min'))
            max_value = float(self.__getDictField(field_valid_values, 'max'))
            lsb_value = float(self.__getDictField(field_valid_values, 'lsb'))

            range_rule_obj = RangeRule('0.0.0.0', min_value, max_value, lsb_value, field_byte_size)
            all_rules.append(range_rule_obj)

        else:

            all_rules = []

        return all_rules




