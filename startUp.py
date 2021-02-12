
from Core.SubsystemParser import SubsystemParser
from GUI.WindowController import WindowController

from Core.ApplicationController import ApplicationController

if __name__ == '__main__':

    all_subsystem_models = []

    # load subsystems into application
    file_path = "/Users/David/PycharmProjects/CommunicationsBus/Assets/Camera.json"
    subsystem_parser = SubsystemParser(file_path)

    x = subsystem_parser.getSubsystem()

    all_subsystem_models.append(subsystem_parser.getSubsystem())

    application_controller = ApplicationController(all_subsystem_models)

    # start-up GUI
    WindowController(application_controller)