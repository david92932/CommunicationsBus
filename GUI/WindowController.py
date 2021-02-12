from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import sys
import ntpath

from GUI.guitest1 import Ui

class WindowController:

    def __init__(self, application_controller):

        self.applicationController = application_controller

        app = QtWidgets.QApplication(sys.argv)
        window = Ui(self.applicationController)

        app.exec_()
