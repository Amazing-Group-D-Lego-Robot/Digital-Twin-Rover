# whole twin system, environment and all

from twin.worldstate import WorldState
from visualisation.server import TwinServer


class TwinSystem:
    def __init__(self, testing=False):
        # print("created a new twin system")

        self.worldstate = WorldState()
        if not testing:
            self.server = TwinServer()
        else:
            self.server = None

    def update(self, sensor_info=None, instruction=None):
        # update the rover with new instruction and sensor info
        # return new updated world state

        self.worldstate.twin.update(sensor_info, instruction, self.worldstate.environment)
        if self.server is not None:
            self.server.update(self.worldstate)

    def predict_next(self, n=1, instruction=None):
        # predict next n time steps of the twin model and returns them with the current environment

        return \
            self.worldstate.twin.predict_next(
                n=n, environment=self.worldstate.environment,
                instruction=instruction), self.worldstate.environment.copy()
