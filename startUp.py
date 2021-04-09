
from Core.SubsystemParser import SubsystemParser
from GUI.WindowController import WindowController

from Core.ScenarioController import ScenarioController

if __name__ == '__main__':

    all_subsystem_models = []

    # load subsystems into application
    file_path = "/Users/David/PycharmProjects/CommunicationsBus/Assets/Camera2.json"
    subsystem_parser = SubsystemParser(file_path)

    x = subsystem_parser.getSubsystem()

    all_subsystem_models.append(subsystem_parser.getSubsystem())

    scenario_controller = ScenarioController(all_subsystem_models)

    # start-up GUI
    WindowController(scenario_controller)