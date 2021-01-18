from PyQt5 import QtWidgets, uic
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
        self.setWindowTitle("% s - Geek PyQt5" % title)
    
    
class MyTableWidget(QtWidgets.QWidget):
    
    def __init__(self, parent):
        self.filesname = "blank"
        super(MyTableWidget, self).__init__(parent)
        uic.loadUi('MyTab.ui', self)
        self.show()
        # Add tabs
    
        
  #  @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
window = Ui()

app.exec_()