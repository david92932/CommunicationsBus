from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import sys
import ntpath

from GUI.guitest1 import Ui

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()

    app.exec_()