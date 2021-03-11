# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 13:51:43 2021

@author: jemac
"""

fieldstring = ""

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
        inFile = open(self.filePath, 'w')
        Lines = inFile.readlines()
        outFile.close()

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
           chunks.pop(1)
           chunks.pop(2)
           chunks.pop(3)

           commandstring1 = line.partition(" ")[2]
           hexnumbers = commandstring1.split(", ")
           i = 0
           for command in available_commands:
                if command.name == commandname:
                    readInCommand = command
                    break

           for field in readInCommand:

                field.value = int(chunks[i], 16)

                i = i + 1
           self.subsystemController.addCommandAtEnd(readInCommand)


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