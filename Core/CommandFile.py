
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
            #these are all the values separated by commas
            chunks = line.split(", ")
            readInCommand = 0
            #line.replace("\n", "")
            commandname = chunks[0]
            commandID = chunks[1]
            commandTime = chunks[2]
            commandNumWords = chunks[3]
            chunks.pop(0)
            chunks.pop(0)
            chunks.pop(0)
            chunks.pop(0)

            commandstring1 = line.partition(" ")[2]
            hexnumbers = commandstring1.split(", ")
            i = 0
            if new_command not in self.subsystemController.getAllAvailableCommands():
                new_command = self.subsystemController.createCommand(commandname)
                #new_command.setTime(commandTime)
            # handle fields with only start/length values
            # handle invalid command names
            # handle command time
                if len(chunks) != 0:
                    for field in new_command.fields:

                     field.setFieldValue(int(chunks[i], 16))

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

            commandstring = f'{command.name}, {command.id}, {command.commandStartField.fieldValue}, {command.wordSizeBits}, '
            for field in command.fields:

                fieldstringhex = hex(int(field.fieldValue))[2:].zfill(field.byteSize * 2)
                # thisfield = bytes(field.byte_size)
                commandstring += "0x" + fieldstringhex + ", "

                commandMainstring = commandMainstring + commandstring[:-2] + "\n"

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
                commandstring += "0x" + fieldstring + ", "

                commandMainstring = commandMainstring + commandstring[:-2] + "\n"
            csv_string = StringIO(commandMainstring)
            df = pd.read_csv(csv_string, sep=", ")
        #df.to_csv(r'Path where you want to store the exported CSV file\File Name.csv')
    # def readCommandString(self, commandstring):
    #     # get/openfile
    #     # remakecommandpart
    #     commandstring1 = commandstring.replace("0x20,", "0x30,")
    #     print(commandstring1)
    #     field1 = fields("haha", 1, 1, 32)
    #     field2 = fields("haha1", 2, 2, 200)
    #     fieldlist = []
    #     fieldlist.append(field1)
    #     fieldlist.append(field2)
    #     command1 = []
    #     command = Command("cameracommand", fieldlist)
    #     command2 = []
    #     command21 = Command("notcameracommand", fieldlist)
    #     command1.append(command)
    #     command1.append(command21)
    #     commandfile = CommandFile("commandfile", command1)
    #
    #     # get commandtype so you now possible fields
    #     # make the command
    #     file1 = open('myfile.tcmd', 'w')
    #     file1.writelines(commandstring1)
    #     file1.close()
    #     file1 = open('myfile.txt', 'r')
    #     Lines = file1.readlines()
    #     # commandname = firstline;
    #     # commandstring2 = commandstring.readlines()
    #     for line in Lines:
    #         line.replace("\n", "")
    #         commandname = line.partition(" ")[0]
    #         commandstring1 = line.partition(" ")[2]
    #         hexnumbers = commandstring1.split(", ")
    #         i = 0
    #         for field in command.fields:
    #             # hexnumbers = commandstring1.split(", ")
    #             field.value = int(hexnumbers[i], 16)
    #
    #             i = i + 1
    #     print(commandfile.commands[0].fields[0].value)
    #     # for values in hexnumbers:
    #     #  field = command.fields[i]
    #     #   field.value = int(values, 16)
    #     # commandfile.commands.fields[i].value = int(values,16)
    #
    #     # i = i+1
    #     # need firstline
    #     # read rest of lines look up command name
    #     # parse fields by comma
    #     # put fields into commmand in order
    #
    #     thiscommand = 1
    #
    #     return thiscommand

    # def main():
    #     field1 = fields("haha", 1, 1, 32)
    #     field2 = fields("haha1", 2, 2, 200)
    #     fieldlist = []
    #     fieldlist.append(field1)
    #     fieldlist.append(field2)
    #     command1 = []
    #     command = Command("cameracommand", fieldlist)
    #     command2 = []
    #     command21 = Command("notcameracommand", fieldlist)
    #     command1.append(command)
    #     command1.append(command21)
    #     commandfile = CommandFile("commandfile", command1)
    #
    #     commandtxt = commandfile.makeCommandString(commandfile)
    #
    #     print(commandfile.makeCommandString(commandfile))
    #     print(commandfile.readCommandString(commandtxt))


    # if __name__ == "__main__":
    #     main()