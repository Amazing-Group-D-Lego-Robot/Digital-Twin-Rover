# whole twin system, environment and all

from visualisation.visualisation import Visualiser

from twin.worldstate import WorldState


class TwinSystem:
    def __init__(self):
        print("created a new twin system")

        self.vis = Visualiser()
        self.worldstate = WorldState()

    def update(self, sensor_info, instruction):
        # update the rover with new instruction and sensor info
        # return new updated world state

        self.worldstate.twin.update(sensor_info, instruction)

    def predict_next(self, n=1, instruction=None):
        # predict next n time steps of the twin model and returns them with the current environment

        return \
            self.worldstate.twin.predict_next(n=n, environment=self.worldstate.environment, instruction=instruction), \
            self.worldstate.environment.copy()
