from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import sys
import ntpath

from GUI.MyTimelineWidget import MyTimelineWidget
from Core.SubsystemSchedule import SubsystemSchedule

class TableView(QTableWidget):
    def __init__(self, file_path, data, *args):

        QTableWidget.__init__(self, *args)

        self.subsystemSchedule = SubsystemSchedule(file_path)
        self.data = self.subsystemSchedule.getSchedule()
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        timeline = MyTimelineWidget(self)

        timeline.addBox(50, 500, 1, "blue")
        timeline.addBox(50, 200, 2, "red")
        self.cellChanged.connect(self.cellUpdated)
        self.show()

    def setData(self):

        schedule_commands = self.subsystemSchedule.getSchedule()
        headers = self.subsystemSchedule.getHeaders()

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

        self.subsystemSchedule.updateCommand(row, column, new_value)