from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import sys
import ntpath
import os

from Core.SubsystemSchedule import SubsystemSchedule

from GUI.MyTimelineWidget import MyTimelineWidget
from GUI.TableView import TableView

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        main_ui_path = os.path.join(os.path.dirname(__file__), 'MainUI.ui')
        uic.loadUi(main_ui_path, self)
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
        file_path, idk = QFileDialog.getOpenFileName()

        file_name = ntpath.basename(file_path)

        self.add_new_tab(file_path, file_name=file_name)

    def add_new_tab(self, file_path, file_name= "No Name Found"):
        data = {'col1': ['1', '2', '3', '4'],
        'col2': ['1', '2', '1', '3'],
        'col3': ['1', '1', '2', '1']}

        # browser = MyTableWidget(self)
        browser = TableView(file_path, data, 4, 8)
        browser.filesname = file_path
        i = self.tabs.addTab(browser, file_name)
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



