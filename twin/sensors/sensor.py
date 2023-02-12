from twin.twin_environment import TwinEnvironment
from twin.twin_model import TwinModel

import numpy as np


class Sensor:
    def __init__(self, name: str):
        self.name = name
        self.value = 0

        # normalised direction vector (0,0,1) is the same direction as the agent is facing)
        self.direction = np.array([0, 0, 1.])
        self.position = np.array([0, 0, 0.])  # offset from agent position

    def update(self, twin: TwinModel, environment: TwinEnvironment):
        pass
