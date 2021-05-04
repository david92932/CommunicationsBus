import os
import sys

from Core.SubsystemParser import SubsystemParser
from GUI.WindowController import WindowController

from Core.ScenarioController import ScenarioController


#Starting Point of Application
if __name__ == '__main__':

    all_subsystem_models = []

    # load subsystems into application
    relative_file_paths = ["AssetsV1/Camera2.json",
                 "AssetsV1/Recorder.json"]

    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):

        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    complete_file_paths = []
    for asset in relative_file_paths:

        config_path = os.path.join(application_path, asset)

        complete_file_paths.append(config_path)


    # build command Subsystem models
    for path in complete_file_paths:
        subsystem_parser = SubsystemParser(path)

        all_subsystem_models.append(subsystem_parser.getSubsystem())

    scenario_controller = ScenarioController(all_subsystem_models)

    # start-up GUI
    WindowController(scenario_controller)