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

        self.cellChanged.connect(self.cellUpdated)
        self.doubleClicked.connect(self.detailedViewExistingCommand)

        screen = QDesktopWidget().screenGeometry()

        self.setMinimumHeight(screen.height()/2)
        self.setMaximumHeight(screen.height() / 2)

        self.setMaximumWidth(screen.width()/1.5)
        self.show()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        exportCommandsAction = menu.addAction("Export File")
        importCommandsAction = menu.addAction("Read File")
        addAboveAction = menu.addAction("Insert Command Above")
        addBelowAction = menu.addAction("Insert Command Below")
        deleteRowAction = menu.addAction("Delete Command")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        row = self.rowAt(event.pos().y())
        if action == importCommandsAction:
            self.subsystemController.readCommandFile('commands.txt')
        if action == exportCommandsAction:
            self.subsystemController.buildCommandFile('commands.txt')
        if action == addAboveAction:
            pass
            # do function to add row
        if action == addBelowAction:
            self.openNewCommandWindow()
        if action == deleteRowAction:
            pass  # do function to delete row

    def testFunc(self):

        pass

    def setData(self):

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

    def cellUpdated(self, row, column):

        new_value = self.item(row, column).text()
        # print(f'changed: {row} {column} {new_value}')

        # self.subsystemSchedule.updateCommand(row, column, new_value)

    def openNewCommandWindow(self):

        self.clearDetailedView()
        self.createDetailedView()

        self.detailedView.createSelectCommand()
        self.showDetailedView()


    def detailedViewChangeEvent(self, value_is_valid, message, binding_function, value):

        if value_is_valid:
            self.setData()
            self.parentObj.setTimeline()
        else:
            self.InvalidErrorBox(message, binding_function, value)

    def showDetailedView(self):

        self.detailedView.show()

    def detailedViewExistingCommand(self, event):

        self.clearDetailedView()
        self.createDetailedView()

        row = event.row()
        command_at_row = self.subsystemController.getSubsystemSchedule()[row]

        self.detailedView.constructDetailedView(command_at_row)

        self.showDetailedView()

    def createDetailedView(self):

        self.detailedView = DetailedView(self.parentObj, self, self.subsystemController)

    def clearDetailedView(self):

        self.detailedView.hide()
        self.detailedView = None

    def InvalidErrorBox(self, message, binding_function, value):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setText(f"Invalid Command Value: {message}")
        msg.setWindowTitle(f"Invalid Command Value: {message}")

        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        msg.buttonClicked.connect(self.errorBoxHandler)

        retval = msg.exec_()

        # print(f'RETVAL: {retval}')

    def errorBoxHandler(self, value):

        print(f"Value: {value.text()}")
