from Core.ScenarioController import ScenarioController
from Core.SubsystemParser import SubsystemParser
from Core.SubsystemController import SubsystemController
from Core.SubsystemParser import Subsystem
import json

current_subsystem = None

def inputParser(userInput):
    if not userInput:
        return

    if "createCamera" in userInput:
        current_subsystem = createCamera()
        return "Camera subsystem created"

    elif "insert" in userInput:

        insertCommand(userInput)

    elif "scenerio" in userInput:

        return scenerio()

    elif "save" in userInput:

        return saveFile(r"C:\Users\Garrett\PycharmProjects\CommunicationsBusApril\Assets\testfile.ccmd")

    elif "exit" in userInput:
        exit()


def help():
    send_message = b"A list of all possible commands are: "
    send_message += SubsystemController.getAllAvailableCommands(SubsystemController.self)
    print("help called")
    conn.sendall(send_message)
    return("Gave user all possible commands")

def createCamera():


    all_subsystem_models = []

    file_path = "/Users/Garrett/PycharmProjects/CommunicationsBusApril/Assets/Camera2.json"
    subsystem_parser = SubsystemParser(file_path)

    all_subsystem_models.append(subsystem_parser.getSubsystem())

    scenario_controller = ScenarioController(all_subsystem_models)

    subsystem_controller = SubsystemController(subsystem_parser.getSubsystem())
    #subsystem_controller.createCommand("Mode")
    # creates camera change power state command, command is added to the subsystem, list of fields are added to array
    # command1 = subsystem_controller.createCommand("Change Power State")


    #Setting fields for first Change Power State command
    #Value for State

    # command1.fields[0].setFieldValue(2)
    #Value for Delay
    # command1.fields[1].setFieldValue(2000)



    #returns a list of command objects
    # print("All commands",subsystem_controller.getAllAvailableCommands())

    #what gets sent to the socket
    send_message = b"made subsystemController Camera"
    #Sending to socket
    conn.sendall(send_message)

    #subsystem_controller.buildCommandFile(r"C:\Users\Garrett\PycharmProjects\CommunicationsBusApril\Assets\test.ccmd")

    print("create camera called")

    return(subsystem_controller)




def insertCommand(input, subsystem_controller):
    #Cuts "insert" from the inputted string
    command = input[6:]
    print("command ",command)

    # what gets sent to the socket
    send_message = b"inserted command "


    if "Mode" in command:
        subsystem_controller.createCommand("Mode")
        send_message += b" mode"
    elif "Change" in command:
        subsystem_controller.createCommand("Change Power State")
        send_message += b" Change Power State"
    elif "Update Status" in command:
        subsystem_controller.createCommand("Update Status")
        send_message += b" Update Status"
    elif "Capture" in command:
        subsystem_controller.createCommand("Capture")
        send_message += b" Capture"

    # Sending to socket
    conn.sendall(send_message)
    return "added command " + command, subsystem_controller


def saveFile(subsystem_controller, file_location_name):

    # Saves to test.ccmd
    #r"C:\Users\Garrett\PycharmProjects\CommunicationsBusApril\Assets\test.ccmd"
    subsystem_controller.buildCommandFile(file_location_name)

    send_message =  b"saved file"
    # Sending to socket
    conn.sendall(send_message)

    return "saved"


# def openScenarioFile(self):
#
#     file_path =
#     self.scenarioController.openScenarioFile(file_path)





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


def exit():
    send_message = b"exit message received, closing socket"
    conn.sendall(send_message)
    conn.close()
    return (send_message)


import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)



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

            if "createCamera" in data:
                current_subsystem = createCamera()
                print("Camera subsystem created")

            elif "insert" in data:
                print("insert called")
                insertCommand(data, current_subsystem)

            elif "scenerio" in data:

                scenerio()

            elif "save" in data:

                saveFile(current_subsystem, r"C:\Users\Garrett\PycharmProjects\CommunicationsBusApril\Assets\testfile.ccmd")

            elif "exit" in data:
                exit()


