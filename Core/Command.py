
from Core.TimelineBox import GraphicsRectItem
from PyQt5 import QtCore, QtGui
from Core.TimelineConfiguration import TimelineConfiguration

class Command:

    def __init__(self, name: str, id: int, command_start_field, command_processing_time, rt_address: int, sub_address: int, word_size_bits: int, protocol: str, fields: []):

        self.name = name
        self.id = id
        self.commandStartField = command_start_field
        self.commandTimeLength: int = 0
        self.rtAddress = rt_address
        self.subAddress = sub_address
        self.wordSizeBits = word_size_bits
        self.processingTime = command_processing_time
        self.protocol = protocol
        self.fields = fields
        self.enabled = True
        self.timelineBox = None
        self.timelineRow = 0
        self.timelineConfiguration = TimelineConfiguration()

        self.__assignFieldsToCommand()

    def getCommandFields(self):

        command_fields = [self.commandStartField]

        command_fields.extend(self.fields)

        return command_fields

    def getCommandFieldsTableView(self):

        command_fields = [self.id, self.commandStartField.getFieldValueEngineeringUnits(), self.wordSizeBits,
                          self.name, self.rtAddress, self.subAddress, self.wordSizeBits, self.enabled]

        return command_fields

    def setStartTime(self, value):

        start_time = self.commandStartField.setFieldValue(value, override_rule_check=True)
        self.calculateLengthTime()
        # self.setTimelineBox()

        return start_time

    def calculateLengthTime(self):

        total_command_length = self.processingTime

        for field in self.fields:
            time_length = field.calculateTimeLength()
            total_command_length += time_length

        self.commandTimeLength = total_command_length

    def getTimeLength(self):

        return self.commandTimeLength

    def setTimelineBox(self):

        self.addBox(self.commandStartField.fieldValue, self.commandTimeLength, self.timelineRow, 'red')

    def addBox(self, startTime, endTime, row, color: str):

        xStartValue = startTime * self.timelineConfiguration.pixelsPerMillisecond
        xEndValue = endTime * self.timelineConfiguration.pixelsPerMillisecond + xStartValue

        yValue = row * (self.timelineConfiguration.boxHeight + self.timelineConfiguration.rowSpacing)

        print(f'start {xStartValue}, end {xEndValue}')
        self.timelineBox = GraphicsRectItem(
            QtCore.QRectF(QtCore.QPointF(xStartValue, yValue), QtCore.QSizeF(xEndValue - xStartValue, self.timelineConfiguration.boxHeight)), command=self)

        self.timelineBox.setBrush(QtGui.QBrush(QtGui.QColor(color)))

    def setTimelineRow(self, row):

        self.timelineRow = row

    def __assignFieldsToCommand(self):
        for field in self.getCommandFields():
            field.ownerCommand = self

    def fieldChangeEvent(self):

        self.calculateLengthTime()
        self.setTimelineBox()

    def validateFields(self):

        rule_violations = []
        for field in self.fields:
            rule_violations.extend(field.validateFieldValue())

        return rule_violations
