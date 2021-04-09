import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

from Core.DefinedValuesRule import DefinedValuesRule
from Core.RangeRule import RangeRule
from Core.TimeRule import TimeRule
from GUI.DetailedViewTextBox import DetailedViewTextBox

from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
    QComboBox,
    QLineEdit
)

from PyQt5.QtWidgets import*

class DetailedView(QWidget):
    def __init__(self, parent, table_view, subsystem_controller):

        super(DetailedView, self).__init__(parent)
        self.parent = parent
        self.tableView = table_view

        self.screen = QDesktopWidget().screenGeometry()
        self.setGeometry(self.screen.width()/1.5, parent.geometry().topLeft().y(), self.screen.width(), self.screen.height()/2)

        # Create a QGridLayout instance
        self.layout = QFormLayout()

        self.subsystemController = subsystem_controller
        self.allCommands = self.subsystemController.getAllAvailableCommands()


    def createSelectCommand(self):

        command_strings = []
        for command in self.allCommands:
            command_strings.append(command.name)

        comboBox = self.createComboBox(command_strings, self.getSelectedCommand)
        comboBox.setFixedWidth(self.screen.width() / 2)

        # self.layout.addWidget(comboBox, 0, 0)
        self.layout.addWidget(comboBox)

        self.setLayout(self.layout)

    def createComboBox(self, list_of_selections, binding_function):

        combo_box = QComboBox()

        for selection in list_of_selections:
            combo_box.addItem(selection)

            # combo_box.activated.connect(binding_function)
        combo_box.currentIndexChanged.connect(binding_function)

        return combo_box

    def createComboBoxWithDescriptions(self, list_of_selections, binding_function, list_of_descriptions, field_changed, field_value):

        combo_box = self.createComboBox(list_of_selections, binding_function)

        if field_changed:

            combo_box.setCurrentIndex(int(field_value))

        for i in range(0, len(list_of_descriptions)):

            combo_box.setItemData(i, list_of_descriptions[i], QtCore.Qt.ToolTipRole)

        return combo_box

    def getSelectedCommand(self, selected_index):
        """
        called when user selects a command from the detailed view dropdown
        Uses the index of the selected command to get the Command object
        that corresponds to the index and calls constructDetailedView()
        and passes the Command object
        :param selected_index: The index of the command selected
        :return:
        """

        selected_command_name = self.allCommands[selected_index].name

        selected_command_obj = self.subsystemController.createCommand(selected_command_name)

        self.constructDetailedView(selected_command_obj)

    def constructDetailedView(self, command_obj):

        all_constructed_boxes_names = []
        all_constructed_boxes = []

        all_fields = command_obj.getCommandFields()

        for field in all_fields:

            field_display_box = None
            field_name_field = None

            is_defined_value_rule_set = False
            is_time_rule = False

            field_value = field.getFieldValueEngineeringUnits()
            field_changed = field.fieldValueChanged

            # for every rule, check if its a defined values rule
            for rule in field.fieldRules:

                if isinstance(rule, DefinedValuesRule):
                    is_defined_value_rule_set = True

                elif isinstance(rule, TimeRule):
                    is_time_rule = True

            # if the field has defined values, create a dropdown for it
            if is_defined_value_rule_set:

                list_of_selections = []
                list_of_descriptions = []

                for rule in field.fieldRules:

                    selection = rule.name
                    list_of_selections.append(selection)
                    description = f'Field Name: {field.name}\nValue: {rule.definedValue} \n' \
                                  f'Description: {field.fieldDescription} \nUnits: {field.fieldUnits}'
                    list_of_descriptions.append(description)

                field_display_box = self.createComboBoxWithDescriptions(list_of_selections, field.setFieldValue, list_of_descriptions, field_changed, field_value)

            # start Time Field
            elif field.fieldRules == []:

                description = f'Field Name: {field.name}\nDescription: {field.fieldDescription}\n' \
                              f'Units: {field.fieldUnits}'

                field_display_box = DetailedViewTextBox(self, field.name, description, command_obj.setStartTime, field_changed, field_value)

            # length field
            elif is_time_rule:

                field_rule = field.fieldRules[0]

                description = f'Field Name: {field.name}\n Min Time: {field_rule.processingTime}\n' \
                              f'Description: {field.fieldDescription}\n' \
                              f'Units: {field.fieldUnits}'

                field_display_box = DetailedViewTextBox(self, field.name, description, command_obj.setLengthTime, field_changed, field_value)

            # if the field is min, max, lsb, create a text box
            else:

                field_rule = field.fieldRules[0]

                description = f'Field Name: {field.name}\nDescription: {field.fieldDescription} \nMin: {field_rule.minValue} \n'\
                              f'Max: {field_rule.maxValue} \nLSB: {field_rule.lsbValue} \nUnits: {field.fieldUnits} '

                field_display_box = DetailedViewTextBox(self, field.name, description, field.setFieldValue, field_changed, field_value)

            field_display_box.setFixedWidth(self.screen.width() / 2)
            all_constructed_boxes_names.append(field.name)
            all_constructed_boxes.append(field_display_box)

        for index, box in enumerate(all_constructed_boxes):

            label = QLabel(all_constructed_boxes_names[index])
            # label.setFixedWidth(self.screen.width() / 4)
            # box.setFixedWidth(self.screen.width() / 4)
            self.layout.addRow(label, box)
            # self.layout.addWidget(box)

        self.setLayout(self.layout)

    def detailedViewChangeEvent(self, value_is_valid, message, binding_function, value):

        self.tableView.detailedViewChangeEvent(value_is_valid, message, binding_function, value)

