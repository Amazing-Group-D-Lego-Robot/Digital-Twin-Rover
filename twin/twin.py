# whole twin system, enviromnet and all

from visualisation.visualisation import Visualiser

class TwinSystem:
    def __init__(self):
        print("created a new twin system")

        vis = Visualiser

    def update(self, sensor_info, instruction):
        # update the rover with new instruction and sensor info
        # return new updated world state
        pass

    def predict_next(self, n=1, instruction=None):
        # predict next n time steps and return them
        pass
