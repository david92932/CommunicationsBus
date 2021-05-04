
"""
Created on Tue Feb  9 13:51:43 2021

@author: jemac
"""
from io import StringIO
import pandas as pd
import csv

class CommandFile:
    """
    Responsible for all file I/O
    """
    def __init__(self, subsystem_controller, file_path):
        """
        :param subsystem_controller: SubsystemController obj to build into a file
        :param file_path: full file location of where to read/write
        """

        self.subsystemController = subsystem_controller
        self.filePath = file_path

    def writeCommandFile(self):
        """
        takes all Commands in self.subsytemController and builds
        command files from them
        :return: writes to a file
        """

        subsystem_schedule = self.subsystemController.getSubsystemSchedule()
        file_string = self.makeCommandString(subsystem_schedule)
        #self.makeCommandCSV(subsystem_schedule)
        #self.readCommandCSV()
        self.writeToFile(file_string)

    def readCommandFile(self):
        """
        read for an existing command file and convert back into python Objs
        to use in the application

        """

        available_commands = self.subsystemController.getAllAvailableCommands()

        inFile = open(self.filePath, 'r')
        Lines = inFile.readlines()
        inFile.close()
        #read in file from Gui
        for line in Lines:
            # these are all the values separated by commas
            #get the values that arent the hex string data
            chunks = line.split(", ")
            readInCommand = 0
            # line.replace("\n", "")
            commandname = chunks[0]
            commandID = chunks[1]
            commandTime = chunks[2]
            commandNumWords = chunks[3]
            #remive data from chunks that isnt hex data
            chunks.pop(0)
            chunks.pop(0)
            chunks.pop(0)
            chunks.pop(0)
            #create a large string with all of the extra characters removed like 0x and commas
            field_values_string = "".join(chunks)
            field_values_string = field_values_string.replace("0x", "")
            field_values_string = field_values_string.replace("\n", "")
            #create a byte array from the string so you can read through based on the byte size and take that size
            # from the array
            bytearray1 = bytearray.fromhex(field_values_string)
            #remove commandid and checksum from message.
            bytearray1 = bytearray1[1:-1]
            print("this is string chunks |" + field_values_string + "|")
            commandstring1 = line.partition(" ")[2]
            hexnumbers = commandstring1.split(", ")
            i = 0

            # check for a command named this in the list of possible commands for its type
            #extract field values from the hexstring based on whehter it is utf8 or a signed/unsigned integer


            command_exists = False
            for command in available_commands:
                if commandname == command.name:
                    command_exists = True
                    break

            if command_exists:
                new_command = self.subsystemController.createCommand(commandname)
                new_command.setStartTime(commandTime)
                # handle fields with only start/length values
                # handle invalid command names
                # handle command time
                y = 0
                if len(chunks) != 0:
                    for field in new_command.fields:
                       # if field.minimum_value < 0:
                       #     field.setFieldValue(
                       #         int.from_bytes(bytearray1[y:y + field.byteSize], byteorder='big', signed=True))
                       # else:
                       if field.fieldRegex:

                           field.setFieldValue(bytearray1[y:y + field.byteSize].decode('utf-8'))

                       elif field.fieldSigned:
                           field.setFieldValue(int.from_bytes(bytearray1[y:y + field.byteSize], byteorder='big', signed=True))
                       else:
                           field.setFieldValue(
                               int.from_bytes(bytearray1[y:y + field.byteSize], byteorder='big', signed=False))

                           y += field.byteSize

                    i = i + 1
                #self.subsystemController.addCommandAtEnd(new_command)

            else:
                raise Exception('Command does not exist')

    # to actually create a command,
    def writeToFile(self, file_string):
        """
        Write file_string into a file
        :param file_string: string of data to write to a file
        :return: N/A
        """

        outFile = open(self.filePath, 'w')
        outFile.writelines(file_string)
        outFile.close()

    def makeCommandCSV(self, all_commands):
        """
        Convert Python Objs into a CSV file
        :param all_commands: Commands to include in CSV file
        :return:
        """
        commandMainstring = "\n"
        #similar to building formatted files except the fields are made into a loarger string with their field names
        #separated by an " = " and are built using engineering values
        for command in all_commands:
            fieldstring = ""
            commandstring = f'{command.name},{command.id},{command.commandStartField.fieldValue},'
            if len(command.fields) == 0:
                fieldstring = "no fields; "
            else:
                for field in command.fields:
                    fieldstring += field.name + " = " + str(field.getFieldValueEngineeringUnits()) + "; "
            commandstring += fieldstring[:-2] + "\n"


            commandMainstring += commandstring[:-1] + "\n"
        #print("command Maind String" + commandMainstring)
        csv_string = StringIO('\n'+commandMainstring)

        df = pd.read_csv(csv_string, sep=",", names=['Commandname', 'commandID', 'starttime', 'fielddata'])
        #df.columns = ['Command name', 'command ID', ' starttime', 'field data']
        #put name value in
        df.to_csv(r'name2.csv')

    def readCommandCSV(self):
        """
        Convert CSV files into Python objects for the appliacation and assign to SubsystemController
        """
        #Essentially the same as reading from the formatted files excpet this uses the engineering values.

        #
        #data = pd.read_csv("name3.csv",sep=",", names=['Commandname', 'commandID', 'starttime', 'fielddata'])
        available_commands = self.subsystemController.getAllAvailableCommands()
        with open('name3.csv', newline='') as File:
            reader = csv.reader(File)
            next(reader)
            for row in reader:
                print("---------------------------------this is row[1]------------------------" +row[1])
                commandname = row[1]
                id = row[2]
                commandTime = row[3]
                fields = row[4]
                chunks = fields.split("; ")
                command_exists = False
                for command in available_commands:
                    if commandname == command.name:
                        command_exists = True
                        break

                if command_exists:
                    new_command = self.subsystemController.createCommand(commandname)
                    new_command.setStartTime(commandTime)
                count = 0
                for field in new_command.fields:
                    #field.chunks[count].split(" = ")[1]
                    field.setFieldValue(chunks[count].split(" = ")[1])
                    count+=1
                #print(commandname)
            #print(row['c1'], row['c2'])


    def makeCommandString(self, all_commands):
        """
        Convert Command Objs to hex strings that can be written to file
        :param all_commands: Command objs to write
        :return: string of data to write to file including all commands
        """
        commandMainstring = ""
        #iterate through all the commands and create formatted strings
        for command in all_commands:

            commandstring = f'{command.name}, {command.id}, {command.commandStartField.fieldValue}, '
            fieldstrings = ""
            fieldstringhex = ""
            for field in command.fields:
                and_value = ""
                formatstring = ""
                intformat = 0

                #create hex strings based on field values and wheter they are string signed or unsigned

                if(field.fieldRegex):
                    s = field.fieldValue.encode('utf-8')
                    fieldstringhex = s.hex()
                    fieldstringhex.zfill(field.byteSize*2)
                   # fieldstringhex= ''.join(['{0:x}'.format(ord(x)) for x in chr(int(field.fieldValue, 16)).encode('utf-8')]).upper()

                    #fieldstringhex  = str(field.fieldValue.encode(encoding = 'UTF-8'))
                elif(field.fieldSigned):
                    and_value = "0x"

                    for i in range(field.byteSize):
                        and_value += "ff"
                        intformat += 2
                    string_format = "0" + str(intformat) + "x"
                    fieldstringhex = format(field.fieldValue & int(and_value, 16), string_format)
                elif(field.fieldSigned == False):
                    fieldstringhex = hex(int(field.fieldValue))[2:].zfill(field.byteSize * 2)
                #
                else:
                    fieldstringhex = ""
                fieldstrings += fieldstringhex
                # commandMainstring = commandMainstring + commandstring[:-2] + "\n"


            # makechecksum
            remainingByte = None
            print("this is fieldstrings" + fieldstringhex)
            hexfill = 255
            fieldstrings = hex(int(command.id))[2:].zfill(2) + fieldstrings
            bytes = bytearray.fromhex(fieldstrings)
            #create checksum and make byte array so you can separate into 2 byte chunks
            sum = 0
            count = 0
            for byte in bytes[:bytes.__len__()]:
                sum = (sum + byte) % 256
                count = count + 1
            checksum = hex(sum ^ 0xFF)[2:].zfill(2)

            # format this sting
            formatline = fieldstrings + checksum
            #commandID_hex = hex(int(command.id))[2:]
            #commandID_hex = hex(int(command.id))[2:].zfill(2)

            #formatline = commandID_hex + formatline
            # for i in range(len(formatline)):
            countbits = 0
            # make 0Xseparatedfields here
            formattedfields = ""
            n = 4  # chunk length
            #create data string and fill if last byte isnt full
            chunks1 = [formatline[i:i + n] for i in range(0, len(formatline), n)]
            for chunks2 in chunks1:
                if len(chunks2) == 2:
                    chunks2 = "00" + chunks2 + ", "
                    countbits += 1
                else:
                    chunks2 = chunks2 + ", "
                    countbits += 1
                formattedfields += "0x" + chunks2
            formattedfields = formattedfields[:-2]

            # if len(fieldstrings) %2 ==0:
            # print(fieldstrings)

            commandMainstring += commandstring + str(countbits) + ", " + formattedfields + "\n"
            # print(commandMainstring)
        return commandMainstring



