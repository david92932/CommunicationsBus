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
    """
    Main UI window
    """
    def __init__(self, scenario_controller):
        """
        Initialize Main GUI Window
        :param scenario_controller: ScenarioController Object with all
        """
        super(Ui, self).__init__()

        self.scenarioController = scenario_controller
        # main_ui_path = os.path.join(os.path.dirname(__file__), 'MainUI.ui')
        relative_ui_path = 'AssetsV1/MainUI.ui'

        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):

            main_ui_path = os.path.dirname(sys.executable)

        elif __file__:
            main_ui_path = os.path.dirname(__file__)

        # needs to point to MainUi.ui file
        complete_ui_path = os.path.join(main_ui_path, relative_ui_path)

        uic.loadUi(complete_ui_path, self)

        self.timeline = MyTimelineWidget(self, self.scenarioController)
        self.tabWidget.setTabsClosable(True)
        self.tabs = self.tabWidget
        self.tabs.currentChanged.connect(self.current_tab_changed) 
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.showMaximized()

        all_subsystem_names = self.scenarioController.getAvailableSubsystemNames()

        self.clearMenuOptions(self.menuOpen)
        self.clearMenuOptions(self.menuFile)
        self.setMenuOptions(self.menuFile, ['Save', 'Save As', 'Save As Scenario'], self.saveMenuHandler)
        self.setMenuOptionsWithParams(self.menuNew, all_subsystem_names, self.newSubsystemHandler)
        self.setMenuOptions(self.menuOpen, ['Open Command File', 'Open Scenario'], self.openMenuHandler)

        self.show()
        self.timeline.show()

    def clearMenuOptions(self, menu_obj):

        menu_obj.clear()

    def setMenuOptions(self, menu_obj, options: [], binding_function):
        """
        set menu_obj to a list of options and when a menu object is called,
        trigger binding_function

        """

        for item in options:
            menu_obj.addAction(item)
        menu_obj.triggered.connect(binding_function)

    def setMenuOptionsWithParams(self, menu_obj, options: [], binding_function):

        menu_obj.clear()

        for item in options:
            entry_name = item
            menu_obj.addAction(item)

        menu_obj.triggered.connect(binding_function)

    def openFile(self):
        """
        Open file handler - calls add_new_tab to create a tab with the opened file
        """

        file_path = self.openFileExplorer()

        if file_path is not None:
            file_name = self.getFileNameFromPath(file_path)
            print('open file')

            self.add_new_tab(file_path=file_path, file_name=file_name)
        
    def openFileExplorer(self, caption=''):
        """
        Open OS file explorer
        :param caption: string to display to user with file
        explorer
        :return: File Path selected by user
        """

        file_path = None
        file_path, idk = QFileDialog.getOpenFileName(caption=caption)

        if file_path == '':
            file_path = None

        return file_path

    def saveFileExplorer(self, caption=''):
        """
        Open OS file explorer for saving
        :param caption: string to display to user with file
        explorer
        :return: File Path selected by user
        """

        file_path = None
        file_path, idk = QFileDialog.getSaveFileName(caption=caption)

        if file_path == '':
            file_path = None

        return file_path

    def getFileNameFromPath(self, file_path):

        return ntpath.basename(file_path)

    def newSubsystemHandler(self, event):
        """
        When a user creates a new subsystem
        """

        self.add_new_tab(new_subsystem_name=event.text())

    def add_new_tab(self, new_subsystem_name="None", file_path="None", file_name="No Name Found", opening_scenario=False):
        """
        Adds a tab with a new tableView on the GUI
        :param new_subsystem_name: Name of new subystem to add - required for new subsystems

        Only required for opening existing:
        :param file_path: File path if user is opening existing file
        :param file_name: Name of file, excluding the path

        If user is opening existing scenario
        :param opening_scenario: Boolean flagging that the user is opening a sceario
        """
        # if we're opening a scenario
        if opening_scenario:

            # Creating subsystem controller for scenarios is handled by ScenarioController,
            # so get all of the active subsystems and create tabs for all of the files
            for subsystem_controller in self.scenarioController.getActiveSubsystems():

                browser = TableView(self, subsystem_controller)

                subsystem_name = subsystem_controller.mySubsystem.subsystemName

                i = self.tabs.addTab(browser, subsystem_name)
                self.tabs.setCurrentIndex(i)

        # if we're creating a new file
        elif file_path == "None":

            new_subsystem_controller = self.scenarioController.createSubsystem(new_subsystem_name)

            browser = TableView(self, new_subsystem_controller)
            browser.filesname = file_path
            i = self.tabs.addTab(browser, new_subsystem_name)
            self.tabs.setCurrentIndex(i)

        # if we're opening an existing file
        else:

            file_extension = file_path.split('.')[1]
            new_subsystem_controller = self.scenarioController.getSubsystemFromFileExtension(file_extension)

            new_subsystem_controller.readCommandFile(file_path)
            browser = TableView(self, new_subsystem_controller)

            i = self.tabs.addTab(browser, file_name)
            self.tabs.setCurrentIndex(i)
    
    def tab_open_doubleclick(self, i): 

        # checking index i.e 
        # No tab under the click 
        if i == -1: 
            # creating a new tab 
            self.add_new_tab()
    def current_tab_changed(self, i): 

        # update the title 
        self.update_title(self.tabs.currentWidget())
       # self.update_title(self.tabs.currentWidget()) 
        
    def close_current_tab(self, i): 

        subsystem_controller = self.getCurrentSubsystemController()
        self.saveHandler(subsystem_controller)
        self.scenarioController.removeActiveSubystemAtIndex(i)
        self.tabs.removeTab(i)

        self.timeline.clearTimelineBoxes()

    def update_title(self, browser): 
  
        # if signal is not from the current tab 
        if browser != self.tabs.currentWidget(): 
            # do nothing 
            return
  
        # get the page title 
        # title = self.tabs.currentWidget().filesname
        title = 'test'

    def setTimeline(self):
        """
        Calls self.timeline object's setTimeline() function
        :return: N/A
        """
        self.timeline.setTimeline()

        self.timeline.show()
        self.timeline.show()

    def getCurrentSubsystemController(self):

        current_index = self.tabs.currentIndex()
        return self.scenarioController.activeSubsystems[current_index]

    def saveAsHandler(self, subsystem_controller):
        """
        Handler for Save as requests
        :param subsystem_controller: SubsystemController obj for subsystem to save

        """

        subystem_name = subsystem_controller.mySubsystem.subsystemName
        file_path = self.saveFileExplorer(caption=f'Enter file path for {subystem_name} subsystem')

        if file_path is not None:

            subsystem_controller.setFilePath(file_path)
            subsystem_controller.buildCommandFile(subsystem_controller.filePath)

        else:

            print('file not saved')

    def saveHandler(self, subsystem_controller):
        """
        Handler for save requests
        :param subsystem_controller: SubsystemController obj for subsystem to save
        """

        if subsystem_controller.filePath == None:
            self.saveAsHandler(subsystem_controller)

        else:
            subsystem_controller.buildCommandFile(subsystem_controller.filePath)

    def saveScenarioHandler(self):
        """
        Handler for saving all open files under 1 scenario
        :return:
        """

        file_path = self.saveFileExplorer(caption="Enter File Path for Scenario")

        # save all active command files
        active_subsystems = self.scenarioController.getActiveSubsystems()
        for subsystem_controller in active_subsystems:

            self.saveHandler(subsystem_controller)

        self.scenarioController.writeScenarioFile(file_path)

    def openSaveWarningDialog(self):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setText("The current file has not been saved")
        msg.setWindowTitle("File Not Saved")

        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.warningDialogBinding)

        retval = msg.exec_()

    def openWarningDialog(self, title, text, binding_function):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setText(title)
        msg.setWindowTitle(text)

        msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)

        msg.buttonClicked.connect(binding_function)

        retval = msg.exec_()

    def warningDialogBinding(self, button_pressed):

        if button_pressed.text() == 'Save':
            subsystem_controller = self.getCurrentSubsystemController()
            self.saveHandler(subsystem_controller)

        else:
            pass

    def saveMenuHandler(self, action):
        """
        Catches events for when a user selects an option from
        the save menu
        :param action: QT event

        """
        button_text = action.text()

        if button_text == 'Save As':
            subsystem_controller = self.getCurrentSubsystemController()
            self.saveAsHandler(subsystem_controller)

        elif button_text == 'Save':
            subsystem_controller = self.getCurrentSubsystemController()
            self.saveHandler(subsystem_controller)

        elif button_text == 'Save As Scenario':
            self.saveScenarioHandler()

    def openMenuHandler(self, action):
        """
        Catches events for when a user selects an option from
        the open menu
        :param action: QT event

        """

        button_text = action.text()

        if button_text == 'Open Command File':
            self.openFile()

        elif button_text == 'Open Scenario':
            self.openScenarioFile()

    def openScenarioFile(self):
        """
        Handler for opening all subsystems in a scenario
        :return: N/A
        """

        file_path = self.openFileExplorer(caption=f'Select scenario file to open')
        self.scenarioController.openScenarioFile(file_path)

        self.add_new_tab(opening_scenario=True)
        self.setTimeline()


