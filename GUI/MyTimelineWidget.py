
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsItem

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

            rect_item = GraphicsRectItem(QtCore.QRectF(QtCore.QPointF(xValue, yValue), QtCore.QSizeF(endTime - startTime, 50)))

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


class GraphicsRectItem(QGraphicsRectItem):

    handleMiddleLeft = 4
    handleMiddleRight = 5

    handleSize = +8.0
    handleSpace = -4.0

    handleCursors = {
        handleMiddleLeft: Qt.SizeHorCursor,
        handleMiddleRight: Qt.SizeHorCursor
    }

    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)
            super().setY(0)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()
        # self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y() - s / 2, s, s)
        # self.handles[self.handleMiddleRight] = QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y(), s, s)
        self.handles[self.handleMiddleRight] = QRectF(b.right() - s, b.center().y(), s, s)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)

        self.prepareGeometryChange()

        if self.handleSelected == self.handleMiddleLeft:

            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleRight:
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        self.updateHandlesPos()

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        painter.setBrush(QBrush(QColor(255, 0, 0, 100)))
        painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        painter.drawRect(self.rect())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                painter.drawEllipse(rect)
