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
    def __init__(self, scenario_controller):
        super(Ui, self).__init__()

        self.scenarioController = scenario_controller
        main_ui_path = os.path.join(os.path.dirname(__file__), 'MainUI.ui')
        uic.loadUi(main_ui_path, self)

        self.timeline = MyTimelineWidget(self, self.scenarioController)
        self.tabWidget.setTabsClosable(True)
        self.tabs = self.tabWidget
        self.tabs.currentChanged.connect(self.current_tab_changed) 
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.actionTempCommand.triggered.connect(lambda: self.openTCMD())
        self.actionVideoCommand.triggered.connect(lambda: self.openCCMD())
        self.actionRecorderCommand.triggered.connect(lambda: self.openRCMD())
        self.showMaximized()

        all_subsystem_names = self.scenarioController.getAvailableSubsystemNames()

        self.clearMenuOptions(self.menuOpen)
        self.clearMenuOptions(self.menuFile)
        self.setMenuOptions(self.menuFile, ['Save', 'Save As'], self.saveMenuHandler)
        self.setMenuOptionsWithParams(self.menuNew, all_subsystem_names, self.add_new_tab)
        self.setMenuOptions(self.menuOpen, all_subsystem_names, self.openFile)

        self.show()
        self.timeline.show()

    def clearMenuOptions(self, menu_obj):
        menu_obj.clear()

    def setMenuOptions(self, menu_obj, options: [], binding_function):

        for item in options:
            menu_obj.addAction(item)
            menu_obj.triggered.connect(binding_function)

    def setMenuOptionsWithParams(self, menu_obj, options: [], binding_function):

        menu_obj.clear()

        for item in options:
            entry_name = item
            menu_obj.addAction(item)
            menu_obj.triggered.connect(lambda item=item: binding_function(new_subsystem=entry_name))

    def openFile(self, name):

        print(f'got to openFile: {name}')

        file_path = self.openFileExplorer()
        file_name = self.getFileNameFromPath(file_path)

        self.add_new_tab(file_path, file_name=file_name)
        
    def openFileExplorer(self):

        file_path, idk = QFileDialog.getOpenFileName()

        return file_path

    def saveFileExplorer(self):

        file_path, idk = QFileDialog.getSaveFileName()

        return file_path

    def getFileNameFromPath(self, file_path):

        return ntpath.basename(file_path)

    def add_new_tab(self, new_subsystem="None", file_path="None", file_name="No Name Found"):

        # if we're creating a new file
        if file_path == "None":

            new_subsystem_controller = self.scenarioController.createSubsystem(new_subsystem)

            browser = TableView(self, new_subsystem_controller)
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
        self.saveHandler()
        self.tabs.removeTab(i)

        
    def update_title(self, browser): 
  
        # if signal is not from the current tab 
        if browser != self.tabs.currentWidget(): 
            # do nothing 
            return
  
        # get the page title 
        # title = self.tabs.currentWidget().filesname
        title = 'test'

    def setTimeline(self):

        self.timeline.setTimeline()

    def getCurrentSubsystemController(self):

        current_index = self.tabs.currentIndex()
        return self.scenarioController.activeSubsystems[current_index]

    def saveAsHandler(self):

        print('save as')
        file_path = self.saveFileExplorer()
        subsystem_controller = self.getCurrentSubsystemController()
        subsystem_controller.setFilePath(file_path)
        subsystem_controller.buildCommandFile(subsystem_controller.filePath)

    def saveHandler(self):

        subsystem_controller = self.getCurrentSubsystemController()
        if subsystem_controller.filePath == None:
            self.saveAsHandler()

        else:
            subsystem_controller.buildCommandFile(subsystem_controller.filePath)

    def openSaveWarningDialog(self):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setText("The current file has not been saved")
        msg.setWindowTitle("File Not Saved")

        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.warningDialogBinding)

        retval = msg.exec_()

    def warningDialogBinding(self, button_pressed):

        print(f'button pressed: {(button_pressed.text())}')
        if button_pressed.text() == 'Save':
            self.saveHandler()

        else:
            pass

    def saveMenuHandler(self, action):
        button_text = action.text()
        if button_text == 'Save As':
            self.saveAsHandler()
        elif button_text == 'Save':
            self.saveHandler()



