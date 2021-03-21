from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
    QComboBox,
    QLineEdit
)

class DetailedViewTextBox(QLineEdit):
    def __init__(self, parent, field_name, description, binding_function, field_changed, field_value):

        super(DetailedViewTextBox, self).__init__(parent)

        self.parent = parent

        self.bindingFunction = binding_function
        self.setToolTip(description)
        self.editingFinished.connect(self.onEditingFinished)

        if not field_changed:
            self.setPlaceholderText(field_name)
            self.setStyleSheet("QCustomLineEdit{color: gray;}")

        else:
            self.setText(str(field_value))

    def onEditingFinished(self):

        self.parent.detailedViewChangeEvent()

        self.bindingFunction(self.text())

