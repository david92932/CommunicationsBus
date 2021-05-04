from Core.ScenarioController import ScenarioController
from Core.SubsystemParser import SubsystemParser
from Core.SubsystemController import SubsystemController
from Core.Command import Command
import socket


def help():
    send_message = b"A list of all possible commands are: "
    send_message += SubsystemController.getAllAvailableCommands(SubsystemController.self)
    print("help called")
    conn.sendall(send_message)
    return("Gave user all possible commands")

def create(input):
    # Cuts "create" from the inputted string
    command = input[6:]
    print_message = b"made subsystemController "

    all_subsystem_models = []
    all_subsystem_names = []

    # load subsystems into application
    file_paths = ["/Users/Garrett/PycharmProjects/CommunicationsBusApril/Assets/Camera2.json",
                  "/Users/Garrett/PycharmProjects/CommunicationsBusApril/Assets/Recorder.json",
                  "/Users/Garrett/PycharmProjects/CommunicationsBusApril/Assets/Temperature.json"]

    for path in file_paths:
        #adding all ICDs to list all_subsystem_models
        subsystem_parser = SubsystemParser(path)
        all_subsystem_models.append(subsystem_parser.getSubsystem())
        all_subsystem_names.append(subsystem_parser.getSubsystem().subsystemName)

    if "Camera" in command:
        subsystem_controller = SubsystemController(all_subsystem_models[0])
        print_message += b" camera"
    elif "Temperature" in command:
        subsystem_controller = SubsystemController(all_subsystem_models[1])
        print_message += b" Temperature"
    elif "Recorder" in command:
        subsystem_controller = SubsystemController(all_subsystem_models[2])
        print_message += b" recorder"
    else:
        print_message = b"Error, invalid system"

    scenario_controller = ScenarioController(all_subsystem_models)



    #subsystem_controller.createCommand("Mode")
    # creates camera change power state command, command is added to the subsystem, list of fields are added to array
    # command1 = subsystem_controller.createCommand("Change Power State")


    #Setting fields for first Change Power State command
    #Value for State

    # command1.fields[0].setFieldValue(2)
    #Value for Delay
    # command1.fields[1].setFieldValue(2000)


    #Sending to socket
    conn.sendall(print_message)

    print(print_message)

    return(subsystem_controller)




def insertCommand(input, subsystem_controller):
    #Cuts "insert" from the inputted string
    command = input[6:]
    print("command ", command)

    # what gets sent to the socket
    send_message = b"inserted command "


    if "Mode" in command:
        return_command = subsystem_controller.createCommand("Mode").getCommandFields()

        send_message += b" mode"
    elif "Change" in command:
        return_command = subsystem_controller.createCommand("Change Power State")
        send_message += b" Change Power State"
    elif "Update Status" in command:
        return_command = subsystem_controller.createCommand("Update Status")
        send_message += b" Update Status"
    elif "Capture" in command:
        return_command = subsystem_controller.createCommand("Capture")
        send_message += b" Capture"

    # Sending to socket
    conn.sendall(send_message)
    return "added command " + command, subsystem_controller, return_command


def saveFile(subsystem_controller, file_location_name):

    subsystem_controller.buildCommandFile(file_location_name)

    send_message =  b"saved file"
    # Sending to socket
    conn.sendall(send_message)

    return "saved"


def scenerio():
    send_message = b"received scenerio request from TCL"

    file_path = "/Users/Garrett/PycharmProjects/CommunicationsBusNewest/Assets/Camera.json"
    subsystem_parser = SubsystemParser(file_path)

    x = subsystem_parser.getSubsystem()

    all_subsystem_models = []
    all_subsystem_models.append(subsystem_parser.getSubsystem())


    scenario_controller = ScenarioController(all_subsystem_models)

    conn.sendall(send_message)
    return ("Hello function called from TCL")


def field(input, command :Command):
    input = input[5:].rstrip()
    field_list = input.split(",")
    print(field_list)
    print(command)
    for command in command:
        print(command.fields)


def exit():
    send_message = b"exit message received, closing socket"
    conn.sendall(send_message)
    conn.close()
    return (send_message)




HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

current_subsystem = None
current_command = None

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        print('You have connected to the Python to TCL testing Socket')
        while True:
        #What TCL sends
            data = conn.recv(1024)

            #Convernting the Bytes to a String
            data = data.decode('utf-8')
            print("Translasted data,", data)

            # inputParser(data)

            if "create" in data:
                current_subsystem = create(data)


            elif "insert" in data:
                current_command = insertCommand(data, current_subsystem)[2]


            elif "field" in data:
                field(data, current_command)

            elif "scenerio" in data:

                scenerio()

            elif "save" in data:

                saveFile(current_subsystem, r"C:\Users\Garrett\PycharmProjects\CommunicationsBusApril\Assets\testfile.ccmd")

            elif "exit" in data:
                exit()


