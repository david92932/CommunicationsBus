
"""
Created on Tue Feb  9 13:51:43 2021

@author: jemac
"""
from io import StringIO
import pandas as pd

class CommandFile:
    def __init__(self, subsystem_controller, file_path):

        self.subsystemController = subsystem_controller
        self.filePath = file_path

    def writeCommandFile(self):

        subsystem_schedule = self.subsystemController.getSubsystemSchedule()
        file_string = self.makeCommandString(subsystem_schedule)
        self.writeToFile(file_string)

    def readCommandFile(self):

        available_commands = self.subsystemController.getAllAvailableCommands()
        inFile = open(self.filePath, 'r')
        Lines = inFile.readlines()
        inFile.close()

        for line in Lines:
            # these are all the values separated by commas
            chunks = line.split(", ")
            readInCommand = 0
            # line.replace("\n", "")
            commandname = chunks[0]
            commandID = chunks[1]
            # commandTime = chunks[2]
            commandNumWords = chunks[3]

            chunks.pop(0)
            chunks.pop(0)
            chunks.pop(0)
            # chunks.pop(0)
            field_values_string = "".join(chunks)
            field_values_string = field_values_string.replace("0x", "")
            field_values_string = field_values_string.replace("\n", "")
            bytearray1 = bytearray.fromhex(field_values_string)
            print("this is string chunks |" + field_values_string + "|")
            commandstring1 = line.partition(" ")[2]
            hexnumbers = commandstring1.split(", ")
            i = 0
            if new_command not in self.subsystemController.getAllAvailableCommands():
                new_command = self.subsystemController.createCommand(commandname)
                # new_command.setTime(commandTime)
                # handle fields with only start/length values
                # handle invalid command names
                # handle command time
                y = 0
                if len(chunks) != 0:
                    for field in new_command.fields:
                        field_byte_size = field.byteSize
                        field.setFieldValue(int(bytearray1[y:y + field_byte_size], 16))
                        y += field_byte_size

                    i = i + 1
                self.subsystemController.addCommandAtEnd(new_command)

    # to actually create a command,
    def writeToFile(self, file_string):

        outFile = open(self.filePath, 'w')
        outFile.writelines(file_string)
        outFile.close()

    def makeCommandString(self, all_commands):
        commandMainstring = ""

        for command in all_commands:

            commandstring = f'{command.name}, {command.id}, {command.wordSizeBits}, '
            fieldstrings = ""
            for field in command.fields:
                fieldstringhex = hex(int(field.fieldValue))[2:].zfill(field.byteSize * 2)
                # thisfield = bytes(field.byte_size)
                # commandstring += "0x" + fieldstringhex + ", "
                fieldstrings += fieldstringhex
                # commandMainstring = commandMainstring + commandstring[:-2] + "\n"


            # makechecksum
            remainingByte = None
            hexfill = 255

            bytes = bytearray.fromhex(fieldstrings)
            sum = 0
            count = 0
            for byte in bytes[:bytes.__len__()]:
                sum = (sum + byte) % 255
                count = count + 1
            checksum = hex(sum ^ 0xFF)[2:].zfill(2)
            print("checksum = 0x" + checksum)
            print("checksum and fields  = 0x" + checksum + fieldstrings)
            # format this sting
            formatline = checksum + fieldstrings
            print("checksum and fields  = 0x" + formatline)
            # for i in range(len(formatline)):

            # make 0Xseparatedfields here
            formattedfields = ""
            n = 4  # chunk length
            chunks1 = [formatline[i:i + n] for i in range(0, len(formatline), n)]
            for chunks2 in chunks1:
                if len(chunks2) != 4:
                    chunks2 = chunks2 + "00"
                else:
                    chunks2 = chunks2 + ", "
                formattedfields += "0x" + chunks2
            print(formattedfields)

            # if len(fieldstrings) %2 ==0:
            # print(fieldstrings)

            commandMainstring += commandstring + formattedfields + "\n"
            # print(commandMainstring)
        return commandMainstring

    def makeCommandCSV(self, all_commands):
        commandMainstring = ""
        for command in all_commands:

            commandstring = f'{command.name}, {command.id}, {command.commandStartField.fieldValue}, {command.wordSizeBits}, '
            for field in command.fields:
                #this is where value needs to be raw
                #fieldstringhex = hex(int(field.fieldValue))[2:].zfill(field.byteSize * 2)
                field_string = field.getFieldValueEngineeringUnits()
                # thisfield = bytes(field.byte_size)
                commandstring += "0x" + field_string + ", "

                commandMainstring = commandMainstring + commandstring[:-2] + "\n"
            csv_string = StringIO(commandMainstring)
            df = pd.read_csv(csv_string, sep=", ")
        df.to_csv(r'Path where you want to store the exported CSV file\File Name.csv')

