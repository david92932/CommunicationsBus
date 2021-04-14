
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import*
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsItem

class MyTimelineWidget(QtWidgets.QGraphicsView):
    def __init__(self, parent, scenario_controller):
        super(MyTimelineWidget, self).__init__(parent)
        self.setScene(QtWidgets.QGraphicsScene(self))

        self.screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, self.screen.height()/2, self.screen.width(),
                         self.screen.height())

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        brush = QtWidgets.QApplication.palette().brush(QtGui.QPalette.Window)
        self.setBackgroundBrush(brush)

        self.scenarioController = scenario_controller

        for x in range(4):
            for i in range(100):
                self.drawLine(100 * i + 100, self.geometry().topLeft().y(), "black")

        self.setTimeline()

    def drawLine(self, xValue, yValue, color):

        rect_item = HorizontalItem(
            QtCore.QRectF(QtCore.QPointF(xValue, yValue), QtCore.QSizeF(2, self.screen.height()/2))
        )

        rect_item.setBrush(QtGui.QBrush(QtGui.QColor(color)))
        self.scene().addItem(rect_item)

    def setTimeline(self):

        self.clearTimelineBoxes()

        subsystem_controllers = self.scenarioController.getActiveSubsystems()

        for subsystem_controller in subsystem_controllers:

            schedule = subsystem_controller.getSubsystemSchedule()
            for command in schedule:

                timeline_box = command.timelineBox
                print(f'tB: {timeline_box}')

                self.scene().addItem(timeline_box)

                print(self.scene().items())

    def clearTimelineBoxes(self):

        for item in list(self.scene().items()):

            if not isinstance(item, HorizontalItem):
                self.scene().removeItem(item)

class HorizontalItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, rect, parent=None):
        super(HorizontalItem, self).__init__(rect, parent)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)


    def itemChange(self, change, value):
        if (
            change == QtWidgets.QGraphicsItem.ItemPositionChange
            and self.scene()
        ):

            # only allow positive x values
            if not (value.x() < 100):
                return QtCore.QPointF(value.x(), self.pos().y())

            else:
                return QtCore.QPointF(0, self.pos().y())

        return super(HorizontalItem, self).itemChange(change, value)

