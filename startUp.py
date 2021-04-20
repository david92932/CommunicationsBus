
from Core.SubsystemParser import SubsystemParser
from GUI.WindowController import WindowController

from Core.ScenarioController import ScenarioController

if __name__ == '__main__':

    all_subsystem_models = []

    # load subsystems into application
    file_paths = ["/Users/David/PycharmProjects/CommunicationsBus/Assets/Camera2.json",
                 "/Users/David/PycharmProjects/CommunicationsBus/Assets/Recorder.json"]

    for path in file_paths:
        subsystem_parser = SubsystemParser(path)

        # x = subsystem_parser.getSubsystem()

        all_subsystem_models.append(subsystem_parser.getSubsystem())

    scenario_controller = ScenarioController(all_subsystem_models)

    # start-up GUI
    WindowController(scenario_controller)