from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('MainUI.ui', self)
        self.tabWidget.setTabsClosable(True)
        self.tabs = self.tabWidget
        self.tabs.currentChanged.connect(self.current_tab_changed) 
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        #self.tab = self.findChild(QtWidgets.tabWidget)
        self.actionTempCommand.triggered.connect(lambda: self.openTCMD())
        self.actionVideoCommand.triggered.connect(lambda: self.openCCMD())
        self.actionRecorderCommand.triggered.connect(lambda: self.openRCMD())
        self.showMaximized()

        self.show()


    def openTCMD(self):
        self.openFileExplorer()
        
        #opentcmdtab
        print("button was pressed")
    
    def openRCMD(self):
        self.openFileExplorer()
        #opentcmdtab
        print("button was pressed")
        
    def openCCMD(self):
        self.openFileExplorer()
        #opentcmdtab
        print("button was pressed")
        
    def openFileExplorer(self):
        filename = QFileDialog.getOpenFileName()
        
        self.add_new_tab(filename)
    def add_new_tab(self, filename, label ="blank" ):
         browser = MyTableWidget(self)
         browser.filesname = filename
         i = self.tabs.addTab(browser, label) 
         print(i)
         self.tabs.setCurrentIndex(i) 
    
    def tab_open_doubleclick(self, i): 
  
        # checking index i.e 
        # No tab under the click 
        if i == -1: 
            # creating a new tab 
            self.add_new_tab()
    def current_tab_changed(self, i): 
  
        # get the curl 
        #qurl = self.tabs.currentWidget().url() 
  
       
        print(i)
        # update the title 
        self.update_title(self.tabs.currentWidget())
       # self.update_title(self.tabs.currentWidget()) 
        
    def close_current_tab(self, i): 
  
        # if there is only one tab 
      
        # else remove the tab 
        self.tabs.removeTab(i) 
        
    def update_title(self, browser): 
  
        # if signal is not from the current tab 
        if browser != self.tabs.currentWidget(): 
            # do nothing 
            return
  
        # get the page title 
        title = self.tabs.currentWidget().filesname
  
        # set the window title 
        # self.setWindowTitle("% s - Geek PyQt5" % title)
        # print("% s - Geek PyQt5" % title)
    
    
class MyTableWidget(QtWidgets.QWidget):
    
    def __init__(self, parent):
        self.filesname = "blank"
        super(MyTableWidget, self).__init__(parent)
        uic.loadUi('MyTab.ui', self)
        timeline = MyTimelineWidget(self)

        timeline.addBox(50, 500, 1, "blue")
        timeline.addBox(50, 200, 2, "red")
        self.show()
        # Add tabs
    
        
  #  @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


class MyTimelineWidget(QtWidgets.QGraphicsView):
    def __init__(self, parent):
        print(parent)
        super(MyTimelineWidget, self).__init__(parent)
        self.setScene(QtWidgets.QGraphicsScene(self))

        print(parent.geometry().width())
        self.setGeometry(0, parent.geometry().bottomLeft().y() + 100, 1500, 300)
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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
window = Ui()

app.exec_()