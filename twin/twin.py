# whole twin system, environment and all
from copy import deepcopy

from twin.worldstate import WorldState
from visualisation.server import TwinServer


class TwinSystem:
    def __init__(self, testing=False):
        # print("created a new twin system")

        self.worldstate = WorldState()
        self.server = None

        if not testing:
            self.server = TwinServer()

    """
    Update the state of the twin system based upon new truth's (sensor data) sent from the rover
    
    Args:
        sensor_info: A pandas dataframe that contains a "timestamp" column, and other labeled sensor columns
        instruction: A String containing the instruction that was just executed to lead to the sensor info
    
    Returns:
        A WorldState object containing the updated world state (used for controller visualisation)
    """
    def update(self, sensor_info=None, instruction=None):
        # update the rover with new instruction and sensor info
        # return new updated world state

        self.worldstate.twin.update(sensor_info, instruction, self.worldstate.environment)
        if self.server is not None:
            self.server.update(self.worldstate)

        return deepcopy(self.worldstate)

    """
    Predict what will happen after executing an instruction

    Args:
        instruction: A String containing the instruction that we want to predict the outcome of executing

    Returns:
        A WorldState object containing the predicted world state (used for controller visualisation)
    """
    def predict_next(self, instruction=None):
        # predict next n time steps of the twin model and returns them with the current environment

        prediction = WorldState()
        prediction.environment = self.worldstate.environment.copy()
        prediction.twin = self.worldstate.twin.predict_next(environment=self.worldstate.environment,
                                                            instruction=instruction)

        return prediction
