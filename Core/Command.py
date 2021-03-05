
from Core.TimelineBox import GraphicsRectItem
from PyQt5 import QtCore, QtGui

class Command:

    def __init__(self, name: str, id: int, command_start_field, command_length_field, rt_address: int, sub_address: int, word_size_bits: int, protocol: str, fields: []):

        self.name = name
        self.id = id
        self.startTime = 0
        self.commandStartField = command_start_field
        self.commandLengthField = command_length_field
        self.rtAddress = rt_address
        self.subAddress = sub_address
        self.wordSizeBits = word_size_bits
        self.protocol = protocol
        self.fields = fields
        self.enabled = True
        self.timelineBox = None

    def getCommandFields(self):

        command_fields = [self.commandStartField, self.commandLengthField]

        command_fields.extend(self.fields)

        return command_fields

    def getCommandFieldsTableView(self):

        command_fields = [self.id, self.commandStartField.fieldValue, self.commandLengthField.fieldValue, self.name,
                          self.rtAddress, self.subAddress, self.wordSizeBits, self.enabled]

        return command_fields

    def setAttribute(self, attribute_name, new_value):

        attribute = getattr(self, attribute_name)

        attribute_type = type(attribute)

        if isinstance(new_value, attribute_type):

            attribute = new_value

        else:

            print(f'New Value {new_value} for attribute {attribute} does not match existing type ({type(new_value)})')

    def setStartTime(self, value):

        print('setstart time')

        self.commandStartField.setFieldValue(value)

    def setLengthTime(self, value):

        print('sets length time')

        self.commandLengthField.setFieldValue(value)

        self.setTimelineBox()

    def setTimelineBox(self):

        self.addBox(self.commandStartField.fieldValue, self.commandLengthField.fieldValue, 1, 'red')

    def addBox(self, startTime, endTime, row, color: str):

        print('add box')
        xValue = startTime + 100
        yValue = row * 75

        self.timelineBox = GraphicsRectItem(
            QtCore.QRectF(QtCore.QPointF(xValue, yValue), QtCore.QSizeF(endTime - startTime, 50)))

        self.timelineBox.setBrush(QtGui.QBrush(QtGui.QColor(color)))
