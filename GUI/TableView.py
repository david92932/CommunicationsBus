from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import sys
import ntpath

from GUI.MyTimelineWidget import MyTimelineWidget
from Core.SubsystemSchedule import SubsystemSchedule
from Core.SubsystemController import SubsystemController
from GUI.DetailedView import DetailedView

class TableView(QTableWidget):
    def __init__(self, parent, subsystem_controller, file_path=None, *args):

        QTableWidget.__init__(self, *args)

        self.parentObj = parent
        self.setRowCount(1)
        self.setColumnCount(8)

        self.subsystemController = subsystem_controller

        self.setData()

        self.createDetailedView()

        # self.cellChanged.connect(self.cellUpdated)
        self.doubleClicked.connect(self.detailedViewExistingCommand)

        screen = QDesktopWidget().screenGeometry()

        self.setMinimumHeight(screen.height()/2)
        self.setMaximumHeight(screen.height() / 2)

        self.setMaximumWidth(screen.width()/1.5)
        self.show()

    def contextMenuEvent(self, event):
        """
        Insertion or Deletion being done

         Keyword arguments: event -- The insert or Delete that is happenning
         """

        menu = QMenu(self)
        addAboveAction = menu.addAction("Insert Command")
        deleteRowAction = menu.addAction("Delete Command")

        action = menu.exec_(self.mapToGlobal(event.pos()))
        row = self.rowAt(event.pos().y())
        if action == addAboveAction:
            self.openNewCommandWindow()
        if action == deleteRowAction:
            pass  # do function to delete row

    def setData(self):

        """ Sets the Data in the Table view"""

        print('table view set data')

        schedule_commands = self.subsystemController.getSubsystemSchedule()
        headers = self.subsystemController.headers

        self.setRowCount(len(schedule_commands))

        for row in range(0, len(schedule_commands)):

            command_in_row = schedule_commands[row]

            for column in range(0, len(headers)):

                cell_data = command_in_row.getCommandFieldsTableView()[column]
                qt_table_widget_item = QTableWidgetItem()
                qt_table_widget_item.setText(str(cell_data))
                # qt_table_widget_item.itemChanged.connect(self.testFunc)

                self.setItem(row, column, qt_table_widget_item)

        self.setHorizontalHeaderLabels(headers)

    def openNewCommandWindow(self):

        """ Opens a new command Window """


        self.clearDetailedView()
        self.createDetailedView()

        self.detailedView.createSelectCommand()
        self.showDetailedView()

    def detailedViewChangeEvent(self, rule_violations_list):

        """
        Updated the detail view from an event changing

        Keyword arguments: rule_violations_list -- A list of any and all rule violations
        """

        print('Table view - detailed view change event')

        for field in rule_violations_list:

            field_name = field.get('fieldName')
            rule_violations = field.get('violations', [])
            field_obj = field.get('fieldObj')

            if rule_violations == []:
                self.setData()
                self.parentObj.setTimeline()

            else:

                for violation in rule_violations:

                    field_valid = violation.get('Valid', False)
                    attempted_value = violation.get('attemptedValue', 0)
                    overridable = violation.get('overridable', False)
                    message = violation.get('message', '')

                    self.InvalidErrorBox(field_name, field_obj, attempted_value, overridable, message)

            self.clearDetailedView()

    def showDetailedView(self):

        """Displays the detailed view"""

        self.detailedView.show()

    def detailedViewExistingCommand(self, event):

        """Displays the detailed View of an existing Command

        Keyword arguments: event -- The command that this function will show the detailed view for
        """

        self.clearDetailedView()
        self.createDetailedView()

        row = event.row()
        command_at_row = self.subsystemController.getSubsystemSchedule()[row]

        self.detailedView.constructDetailedView(command_at_row, command_exist=True)

        self.showDetailedView()

    def createDetailedView(self):

        """Creates a mew detailed View"""

        self.detailedView = DetailedView(self.parentObj, self, self.subsystemController)

    def clearDetailedView(self):

        """Clears the Detailed View"""

        # if self.detailedView is not None:
        self.detailedView.clearDetailedView()
            # self.detailedView = None

    def InvalidErrorBox(self, field_name, field_obj, attempted_value, overridable, message):

        """Creates an error box describing what went wrong

               Keyword arguments: field_name -- The Field that is having the error
               field_obj -- The object connected to the field in question
               attempted_value -- The value the user inputted
               overridable -- Is this value able to be input anyways?
               message -- What is displayed to the user
               """

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setText(f"Invalid field value for field: \'{field_name}\' \n {message}")

        msg.setWindowTitle(f"Invalid Field Value")

        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        if msg.exec() == QMessageBox.Ok:

            if overridable:
                field_obj.setFieldValue(attempted_value, override_rule_check=True)

        else:
            print('selected cancel')

    def errorBoxHandler(self, msg_button, attempted_value, overridable, field_obj):
        """The handler for the error box

                     Keyword arguments: msg_button -- the button to accept or deny
                     field_obj -- The object connected to the field in question
                     attempted_value -- The value the user inputted
                     overridable -- Is this value able to be input anyways?

                     """

        retval = msg_button.exec_()
        print('error Box Handler')
        print(retval)


