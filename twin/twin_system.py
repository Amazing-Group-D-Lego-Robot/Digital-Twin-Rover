# whole twin system, environment and all
from copy import deepcopy

from twin.twin_designs.debug_twin import DebugTwinModel
from twin.twin_designs.dumb_twin import DumbTwinModel
from twin.twin_environment import TwinEnvironment


class TwinSystem:
    def __init__(self):
        self.environment = TwinEnvironment()
        self.twin = DumbTwinModel()

    def change_instruction(self, instruction: str):
        """
        Changes the current instruction being executed. Run this at the start of every new instruction!
        :param instruction:
        :return:
        """
        self.twin.change_instruction(instruction)

    def update(self, sensor_info=None):
        """
        Update the state of the twin system based upon new truth's (sensor data) sent from the rover

        :param sensor_info: A pandas dataframe that contains a "timestamp" column, and other labeled sensor columns
        :returns: A WorldState object containing the updated world state (used for controller visualisation)
        """
        # update the rover with new instruction and sensor info
        # return new updated world state

        self.twin.update(sensor_info, self.environment)

        return self.twin.copy(), self.environment.copy()

    def predict_next(self, instructions=None):
        """
        Predict what will happen after executing an instruction

        :param instructions: A list of string instructions to predict the execution of
        :type instructions: list
        :rtype list:
        :returns: List of timestamped WorldStates for each prediction step
        """
        # predict next n time steps of the twin model and returns them with the current environment

        environment = self.environment.copy()
        prediction = self.twin.predict_next(environment=self.environment, instructions=instructions)

        return environment, prediction
