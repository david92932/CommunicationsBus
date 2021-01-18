from PyQt5 import QtCore, QtGui, QtWidgets


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
            return QtCore.QPointF(value.x(), self.pos().y())
        return super(HorizontalItem, self).itemChange(change, value)


class Widget(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setScene(QtWidgets.QGraphicsScene(self))
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        brush = QtWidgets.QApplication.palette().brush(QtGui.QPalette.Window)
        self.setBackgroundBrush(brush)

        for i in range(3):

            xValue = 0
            yValue = i * 100

            rect_item = HorizontalItem(
                QtCore.QRectF(QtCore.QPointF(xValue, yValue), QtCore.QSizeF(200, 50))
            )
            rect_item.setBrush(QtGui.QBrush(QtGui.QColor("red")))
            self.scene().addItem(rect_item)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.setMinimumSize(640, 480)
    w.show()
    sys.exit(app.exec_())