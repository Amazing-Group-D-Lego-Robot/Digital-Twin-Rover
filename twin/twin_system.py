# whole twin system, environment and all
from copy import deepcopy

from twin.twin_designs.debug_twin import DebugTwinModel
from twin.twin_environment import TwinEnvironment


class TwinSystem:
    def __init__(self):
        self.environment = TwinEnvironment()
        self.twin = DebugTwinModel()

    def update(self, sensor_info=None, instruction=None):
        """
        Update the state of the twin system based upon new truth's (sensor data) sent from the rover

        :param sensor_info: A pandas dataframe that contains a "timestamp" column, and other labeled sensor columns
        :param instruction: A String containing the instruction that was just executed to lead to the sensor info
        :returns: A WorldState object containing the updated world state (used for controller visualisation)
        """
        # update the rover with new instruction and sensor info
        # return new updated world state

        self.twin.update(sensor_info, instruction, self.environment)

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
        twin = self.twin.predict_next(environment=self.environment, instructions=instructions)

        return environment, twin
