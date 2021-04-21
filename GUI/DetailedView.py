import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

from Core.DefinedValuesRule import DefinedValuesRule
from Core.RangeRule import RangeRule
from Core.TimeRule import TimeRule
from GUI.DetailedViewTextBox import DetailedViewTextBox
from Core.RegexRule import RegexRule

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

        self.constructedBoxes = []
        self.constructedBoxFieldObjs = []


    def createSelectCommand(self):

        command_strings = []
        for command in self.allCommands:
            command_strings.append(command.name)

        comboBox = self.createComboBox(command_strings, self.getSelectedCommand)
        comboBox.setFixedWidth(self.screen.width() / 2)

        # self.layout.addWidget(comboBox, 0, 0)
        self.layout.addWidget(comboBox)

        self.setLayout(self.layout)

    def createComboBox(self, list_of_selections, binding_function=None):

        combo_box = QComboBox()

        for selection in list_of_selections:
            combo_box.addItem(selection)

            # combo_box.activated.connect(binding_function)
        if binding_function is not None:
            combo_box.currentIndexChanged.connect(binding_function)

        return combo_box

    def createComboBoxWithDescriptions(self, list_of_selections, binding_function, list_of_descriptions, field_value, field_changed):

        combo_box = self.createComboBox(list_of_selections)

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

        self.clearDetailedView()

        selected_command_obj = self.allCommands[selected_index]
        selected_command_name = selected_command_obj.name

        self.selectedCommandObj = self.subsystemController.createCommandWithoutAdding(selected_command_name)

        self.constructDetailedView(self.selectedCommandObj)

    def constructDetailedView(self, command_obj, command_exist=False):

        if command_exist:

            self.selectedCommandObj = command_obj

        self.constructedBoxes = []
        self.constructedBoxFieldObjs = []

        all_fields = command_obj.getCommandFields()

        for field in all_fields:

            field_display_box = None
            field_name_field = None

            is_defined_value_rule_set = False
            is_time_rule = False
            is_regex_rule = False

            field_value = field.getFieldValueEngineeringUnits()
            field_changed = field.fieldValueChanged

            # for every rule, check if its a defined values rule
            for rule in field.fieldRules:

                if isinstance(rule, DefinedValuesRule):
                    is_defined_value_rule_set = True

                elif isinstance(rule, TimeRule):
                    is_time_rule = True

                elif isinstance(rule, RegexRule):
                    is_regex_rule = True

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

                field_display_box = self.createComboBoxWithDescriptions(list_of_selections, field.setFieldValue, list_of_descriptions, field_value, command_exist)

            # start Time Field
            elif field.fieldRules == []:

                description = f'Field Name: {field.name}\nDescription: {field.fieldDescription}\n' \
                              f'Units: {field.fieldUnits}'

                field_display_box = DetailedViewTextBox(self, field.name, description, command_obj.setStartTime, field_value, command_exist)

            elif isinstance(field.fieldRules[0], RegexRule):

                field_rule = field.fieldRules[0]
                description = f'Field Name: {field.name}\nDescription: {field.fieldDescription} \n Regex Expression: {field_rule.regexExpression} '

                field_display_box = DetailedViewTextBox(self, field.name, description, field.setFieldValue, field_value,
                                                        command_exist)

            # if the field is min, max, lsb, create a text box
            else:

                field_rule = field.fieldRules[0]

                description = f'Field Name: {field.name}\nDescription: {field.fieldDescription} \nMin: {field_rule.minValue} \n'\
                              f'Max: {field_rule.maxValue} \nLSB: {field_rule.lsbValue} \nUnits: {field.fieldUnits} '

                field_display_box = DetailedViewTextBox(self, field.name, description, field.setFieldValue, field_value, command_exist)

            field_display_box.setFixedWidth(self.screen.width() / 2)
            self.constructedBoxFieldObjs.append(field)
            self.constructedBoxes.append(field_display_box)

        for index, box in enumerate(self.constructedBoxes):

            label = QLabel(self.constructedBoxFieldObjs[index].name)
            # label.setFixedWidth(self.screen.width() / 4)
            # box.setFixedWidth(self.screen.width() / 4)
            self.layout.addRow(label, box)
            # self.layout.addWidget(box)

        cancel_button = QPushButton(text='Cancel')
        cancel_button.clicked.connect(self.clearDetailedView)
        confirm_button = QPushButton(text='Confirm')
        confirm_button.clicked.connect(lambda: self.confirmDetailedView(command_exist))

        self.layout.addRow(cancel_button, confirm_button)
        self.setLayout(self.layout)

    def detailedViewChangeEvent(self, rule_violations_list):

        print('detailed view change event')
        self.tableView.detailedViewChangeEvent(rule_violations_list)

    def clearDetailedView(self):

        self.constructedBoxes = []
        self.constructedBoxFieldObjs = []
        self.selectedCommandObj = None

        self.clearLayout()

    def confirmDetailedView(self, command_exists: bool):

        selected_command_name = self.selectedCommandObj.name
        print(f'confirm detailed view - Command: {selected_command_name}')

        all_rule_violations = []

        # add command if it doesn't exist
        if not command_exists:
            self.subsystemController.addCommandAtEnd(self.selectedCommandObj)

        for index, field_box in enumerate(self.constructedBoxFieldObjs):

            qt_form_box = self.constructedBoxes[index]

            if isinstance(qt_form_box, QComboBox):

                text = qt_form_box.currentIndex()

            else:

                text = qt_form_box.text()

            field_rule_violations_dict = field_box.setFieldValue(text)

            all_rule_violations.append(field_rule_violations_dict)

        self.selectedCommandObj.fieldChangeEvent()
        self.selectedCommandObj.setTimelineBox()

        self.detailedViewChangeEvent(all_rule_violations)

    def clearLayout(self):
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)

            if not item:
                continue

            w = item.widget()
            if w:
                w.deleteLater()