from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
    QComboBox,
    QLineEdit
)

class DetailedViewTextBox(QLineEdit):
    def __init__(self, parent, field_name, description, binding_function):

        super(DetailedViewTextBox, self).__init__(parent)

        self.parent = parent

        self.bindingFunction = binding_function
        self.setToolTip(description)
        self.editingFinished.connect(self.onEditingFinished)

        self.setPlaceholderText(field_name)
        self.setStyleSheet("QCustomLineEdit{color: gray;}")

    def onEditingFinished(self):

        self.parent.detailedViewChangeEvent()

        self.bindingFunction(self.text())

