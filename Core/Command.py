
from Core.TimelineBox import GraphicsRectItem
from PyQt5 import QtCore, QtGui
from Core.TimelineConfiguration import TimelineConfiguration

class Command:
    """
    Class represents a single subystem command
    """

    def __init__(self, name: str, id: int, command_start_field, command_processing_time, rt_address: int, sub_address: int, word_size_bits: int, protocol: str, fields: []):
        """
        Command objs are built by SubsytemParser on startUp
        :param name: name of command
        :param id: command ID
        :param command_start_field: Field obj for start time of command
        :param command_processing_time: mandatory time to process command
        :param rt_address: RT address
        :param sub_address: Sub address
        :param word_size_bits: Size of command in bits
        :param protocol: Communication Protocol used by command
        :param fields: list of Field objs that are included in the Command
        """
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
        self.timelineColor = 'red'

        self.__assignFieldsToCommand()

    def getCommandFields(self):
        """
        returns list of all Fields associated with command
        :return:
        """

        command_fields = [self.commandStartField]

        command_fields.extend(self.fields)

        return command_fields

    def getCommandFieldsTableView(self):
        """
        returns all values to display on table row for Command
        """

        command_fields = [self.id, self.commandStartField.getFieldValueEngineeringUnits(), self.wordSizeBits,
                          self.name, self.rtAddress, self.subAddress, self.wordSizeBits, self.enabled]

        return command_fields

    def setStartTime(self, value):
        """
        Set the start time of the command
        :param value: time in ms
        """

        start_time = self.commandStartField.setFieldValue(value, override_rule_check=True)
        self.calculateLengthTime()
        self.setTimelineBox()

        return start_time

    def calculateLengthTime(self):
        """
        Iterates through all command fields to determine if they
        affect the command's length
        :return: returns value of the command's time in ms
        """

        total_command_length = self.processingTime

        for field in self.fields:
            time_length = field.calculateTimeLength()
            total_command_length += time_length

        self.commandTimeLength = total_command_length
        return total_command_length

    def getTimeLength(self):

        return self.commandTimeLength

    def setTimelineBox(self):

        self.addBox(self.commandStartField.fieldValue, self.calculateLengthTime(), self.timelineRow, self.timelineColor)

    def addBox(self, startTime, endTime, row, color: str):
        """
        Creates a GraphicsRectItem that will appear on the timeline
        :param startTime: time of command start
        :param endTime: time of command end
        :param row: The timeline row to assign to this timeline box (positive integer)
        (row 0 is top)
        :param color: Color of timeline box - doesn't work
        :return: N/A - assigns self.timelineBox to the created obj
        """

        xStartValue = startTime * self.timelineConfiguration.pixelsPerMillisecond
        xEndValue = endTime * self.timelineConfiguration.pixelsPerMillisecond + xStartValue

        yValue = row * (self.timelineConfiguration.boxHeight + self.timelineConfiguration.rowSpacing)

        self.timelineBox = GraphicsRectItem(
            QtCore.QRectF(QtCore.QPointF(xStartValue, yValue), QtCore.QSizeF(xEndValue - xStartValue, self.timelineConfiguration.boxHeight)), command=self)

        self.timelineBox.setBrush(QtGui.QBrush(QtGui.QColor(color)))

    def setTimelineRow(self, row):

        self.timelineRow = row

    def __assignFieldsToCommand(self):
        for field in self.getCommandFields():
            field.ownerCommand = self

    def fieldChangeEvent(self):
        """
        When a field is changed, an event is cascaded from Field
        to handle the event and display updated info on the GUI
        :return:
        """

        self.calculateLengthTime()
        self.setTimelineBox()

    def validateFields(self):
        """
        Function calls validateFieldValue for all Fields
        associated with this Command
        :return: list of dict rule violations (see Field)
        """

        rule_violations = []
        for field in self.fields:
            rule_violations.extend(field.validateFieldValue())

        return rule_violations

    def setTimelineColor(self, color: str):

        self.timelineColor = color