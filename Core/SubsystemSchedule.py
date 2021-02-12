from Core.Command import Command

class SubsystemSchedule:

    def __init__(self, file_path):

        self.filePath = file_path
        self.commands = []

        self.headers = ['BusEm Id', 'BusEm Start', 'BusEm Length', 'Command Name', 'RT Address',
                        'Sub Address', 'Word Count', 'Enabled']

    def updateCommand(self, row, column, new_value):

        command_to_update = self.getCommandFromRow(row)

        command_to_update.updateCommand(column, new_value)

    def getSchedule(self):

        return self.commands

    def getHeaders(self):

        return self.headers

    def getCommandFromRow(self, row):

        return self.commands[row]

