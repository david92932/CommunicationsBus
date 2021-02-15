from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import sys
import ntpath
import os

from GUI.MyTimelineWidget import MyTimelineWidget
from GUI.TableView import TableView

class Ui(QtWidgets.QMainWindow):
    def __init__(self, application_controller):
        super(Ui, self).__init__()

        self.applicationController = application_controller

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

        all_subsystem_names = self.getAvailableSubsystems()
        self.setCreateNewMenuOptions(self.menuNew, all_subsystem_names, self.add_new_tab)
        self.setMenuOptions(self.menuOpen, all_subsystem_names, self.openFile)
        self.show()

    def setMenuOptions(self, menu_obj, options: [], binding_function):

        menu_obj.clear()

        for item in options:
            menu_obj.addAction(item)
            menu_obj.triggered.connect(lambda item=item: binding_function())

    def setCreateNewMenuOptions(self, menu_obj, options: [], binding_function):

        menu_obj.clear()

        for item in options:
            entry_name = item
            menu_obj.addAction(item)
            menu_obj.triggered.connect(lambda item=item: binding_function(new_subsystem=entry_name))

    def openFile(self, name):

        print(f'got to openFile: {name}')

        self.openFileExplorer()
        
    def openFileExplorer(self):

        file_path, idk = QFileDialog.getOpenFileName()

        file_name = ntpath.basename(file_path)

        self.add_new_tab(file_path, file_name=file_name)

    def add_new_tab(self, new_subsystem="None", file_path="None", file_name= "No Name Found"):

        data = {'col1': ['1', '2', '3', '4'],
        'col2': ['1', '2', '1', '3'],
        'col3': ['1', '1', '2', '1']}

        # if we're creating a new file
        if file_path == "None":

            browser = TableView(self.applicationController, new_subsystem, file_path, data, 4, 8)
            browser.filesname = file_path
            i = self.tabs.addTab(browser, new_subsystem)
            self.tabs.setCurrentIndex(i)

        # if we're opening an existing file
        else:

            # doesn't work yet
            # browser = TableView(self.applicationController, file_path, data, 4, 8)
            # browser.filesname = file_path
            # i = self.tabs.addTab(browser, file_path)
            # self.tabs.setCurrentIndex(i)

            pass


    
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
        # title = self.tabs.currentWidget().filesname
        title = 'test'

    def getAvailableSubsystems(self):

        all_names = []

        for subsystem in self.applicationController.allSubsystems:

            all_names.append(subsystem.subsystemName)

        return all_names



