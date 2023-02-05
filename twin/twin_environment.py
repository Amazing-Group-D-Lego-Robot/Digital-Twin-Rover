from copy import deepcopy


class TwinEnvironment:
    def __init__(self):
        self.observed_points = []  # All points that the agent has "seen" with sensors
        self.world = []  # All pre-programmed tris representing the world

    def copy(self):
        # copy function for making predictions
        return deepcopy(self)
