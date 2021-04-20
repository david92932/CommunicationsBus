from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
    QComboBox,
    QLineEdit
)

class DetailedViewTextBox(QLineEdit):
    def __init__(self, parent, field_name, description, binding_function, field_value, command_exists):

        super(DetailedViewTextBox, self).__init__(parent)

        self.parent = parent
        self.fieldName = field_name
        self.description = description
        self.bindingFunction = binding_function
        self.setToolTip(description)
        # self.editingFinished.connect(self.onEditingFinished)

        if not command_exists:

            self.setCustomPlaceholderText()

        else:
            self.setText(str(field_value))

    def onEditingFinished(self):

        value = self.text()
        # value_is_valid, message = self.bindingFunction(self.text())
        # x = self.bindingFunction(self.text())

        # print(f'X: {x}')
        # self.parent.detailedViewChangeEvent(value_is_valid, message, self.bindingFunction, value)

    def setCustomPlaceholderText(self, text: str = None):

        if text is None:
            text = self.fieldName

        self.setPlaceholderText(text)
        self.setStyleSheet("QCustomLineEdit{color: gray;}")