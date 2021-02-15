import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

from Core.DefinedValuesRule import DefinedValuesRule
from Core.RangeRule import RangeRule
from GUI.DetailedViewTextBox import DetailedViewTextBox

from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
    QComboBox,
    QLineEdit
)

class DetailedView(QWidget):
    def __init__(self, parent, subsystem_controller):

        # super().__init__()
        super(DetailedView, self).__init__(parent)
        # Create a QGridLayout instance
        self.layout = QGridLayout()

        self.subsystemController = subsystem_controller
        self.allCommands = self.subsystemController.getAllAvailableCommands()

        command_strings = []
        for command in self.allCommands:
            command_strings.append(command.name)

        comboBox = self.createComboBox(command_strings, self.getSelectedCommand)
        self.layout.addWidget(comboBox, 0, 0)
        # Add widgets to the layout
        # layout.addWidget(QPushButton("Button at (0, 0)"), 0, 0)
        # layout.addWidget(QPushButton("Button at (0, 1)"), 0, 1)
        # layout.addWidget(QPushButton("Button at (0, 2)"), 0, 2)
        # layout.addWidget(QPushButton("Button at (1, 0)"), 1, 0)
        # layout.addWidget(QPushButton("Button at (1, 1)"), 1, 1)
        # layout.addWidget(QPushButton("Button at (1, 2)"), 1, 2)
        # layout.addWidget(QPushButton("Button at (2, 0)"), 2, 0)
        # layout.addWidget(QPushButton("Button at (2, 1)"), 2, 1)
        # layout.addWidget(QPushButton("Button at (2, 2)"), 2, 2)
        # Set the layout on the application's window
        self.setLayout(self.layout)

        self.setGeometry(0, parent.geometry().bottomLeft().y()-300, 1500, 100)

        # self.show()

    def createComboBox(self, list_of_selections, binding_function):

        combo_box = QComboBox()

        for selection in list_of_selections:
            combo_box.addItem(selection)
            combo_box.activated.connect(binding_function)

        return combo_box

    def createComboBoxWithDescriptions(self, list_of_selections, binding_function, list_of_descriptions):

        combo_box = self.createComboBox(list_of_selections, binding_function)

        for i in range(0, len(list_of_descriptions)):

            combo_box.setItemData(i, list_of_descriptions[i], QtCore.Qt.ToolTipRole)

        return combo_box

    def getSelectedCommand(self, selected_index):
        """
        called when user selects a command from the detailed view dropdown
        Uses the index of the selected command to get the Command object
        that corresponds to the index and calls __constructDetailedView()
        and passes the Command object
        :param selected_index: The index of the command selected
        :return:
        """

        print(f'event - {selected_index}')
        selected_command_obj = self.allCommands[selected_index]

        self.__constructDetailedView(selected_command_obj)

        #deep copy command and add

    def __constructDetailedView(self, command_obj):

        all_constructed_boxes = []

        all_fields = command_obj.fields

        for field in all_fields:

            field_display_box = None

            is_defined_value_rule_set = False

            # for every rule, check if its a defined values rule
            for rule in field.fieldRules:

                if isinstance(rule, DefinedValuesRule):
                    is_defined_value_rule_set = True
                    break

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


                field_display_box = self.createComboBoxWithDescriptions(list_of_selections, field.setFieldValue, list_of_descriptions)

            # if the field is min, max, lsb, create a text box
            else:

                field_rule = field.fieldRules[0]

                description = f'Field Name: {field.name}\nDescription: {field.fieldDescription} \nMin: {field_rule.minValue} \n'\
                              f'Max: {field_rule.maxValue} \nLSB: {field_rule.lsbValue} \nUnits: {field.fieldUnits} '

                field_display_box = DetailedViewTextBox(self, field.name, description, field.setFieldValue)

            all_constructed_boxes.append(field_display_box)

        for index, box in enumerate(all_constructed_boxes):

            self.layout.addWidget(box, 0, index)


    def __getSelectedDefinedRule(self, selected_index):

        pass
