from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import sys
import ntpath

class MyTimelineWidget(QtWidgets.QGraphicsView):
    def __init__(self, parent):
        print(parent)
        super(MyTimelineWidget, self).__init__(parent)
        self.setScene(QtWidgets.QGraphicsScene(self))

        print(parent.geometry().width())
        self.setGeometry(0, parent.geometry().bottomLeft().y(), 1500, 300)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        brush = QtWidgets.QApplication.palette().brush(QtGui.QPalette.Window)
        self.setBackgroundBrush(brush)

        for x in range(4):
            for i in range(100):
                self.drawLine(100 * i + 100, parent.geometry().topLeft().y(), "black")

    def addBox(self, startTime, endTime, row, color: str):

            xValue = startTime + 100
            yValue = row * 75

            rect_item = HorizontalItem(
                QtCore.QRectF(QtCore.QPointF(xValue, yValue), QtCore.QSizeF(endTime - startTime, 50))
            )
            rect_item.setBrush(QtGui.QBrush(QtGui.QColor(color)))
            self.scene().addItem(rect_item)

    def drawLine(self, xValue, yValue, color):

            rect_item = HorizontalItem(
                QtCore.QRectF(QtCore.QPointF(xValue, yValue), QtCore.QSizeF(2, 300))
            )

            rect_item.setBrush(QtGui.QBrush(QtGui.QColor(color)))
            self.scene().addItem(rect_item)

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


class VerticalLine(QtWidgets.QGraphicsRectItem):
    def __init__(self, rect, parent=None):
        super(VerticalLine, self).__init__(rect, parent)

    def drawLine(self, xValue, yValue, height):

        rect_item = HorizontalItem(
            QtCore.QRectF(QtCore.QPointF(xValue, yValue), QtCore.QSizeF(2, height))
        )

        rect_item.setBrush(QtGui.QBrush(QtGui.QColor("red")))
        self.scene().addItem(rect_item)