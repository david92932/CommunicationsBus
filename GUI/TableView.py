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
    def __init__(self, application_controller, new_subsystem, file_path, data, *args):

        QTableWidget.__init__(self, *args)

        self.setRowCount(1)
        self.setColumnCount(8)

        self.applicationController = application_controller


        self.subsystemController = SubsystemController(new_subsystem, application_controller.allSubsystems)
        self.data = None
        self.setData()

        timeline = MyTimelineWidget(self)


        timeline.addBox(50, 500, 1, "blue")
        timeline.addBox(50, 200, 2, "red")
        self.cellChanged.connect(self.cellUpdated)


        self.show()
        # detailed.show()


    def contextMenuEvent(self, event):
        menu = QMenu(self)
        addAboveAction = menu.addAction("Insert Command Above")
        addBelowAction = menu.addAction("Insert Command Below")
        deleteRowAction = menu.addAction("Delete Command")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        row = self.rowAt(event.pos().y())
        print(f'row: {row}')
        if action == addAboveAction:
            pass
            # do function to add row
        if action == addBelowAction:
            self.openNewCommandWindow()
        if action == deleteRowAction:
            pass  # do function to delete row

    def setData(self):

        schedule_commands = self.subsystemController.getSubsystemSchedule()
        headers = self.subsystemController.headers

        for row in range(0, len(schedule_commands)):

            command_in_row = schedule_commands[row]

            for column in range(0, len(headers)):

                cell_data = command_in_row.getCommandPropertyList()[column]
                qt_table_widget_item = QTableWidgetItem()
                qt_table_widget_item.setText(str(cell_data))

                print(f'Data: {qt_table_widget_item.text()}')
                self.setItem(row, column, qt_table_widget_item)

        self.setHorizontalHeaderLabels(headers)

    def cellUpdated(self, row, column):

        new_value = self.item(row, column).text()
        print(f'changed: {row} {column} {new_value}')

        # self.subsystemSchedule.updateCommand(row, column, new_value)

    def openNewCommandWindow(self):

        detailedView = DetailedView(self, self.subsystemController)
        detailedView.show()



