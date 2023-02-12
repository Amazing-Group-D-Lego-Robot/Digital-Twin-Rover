import numpy as np

from twin.sensors.sensor import Sensor
from twin.twin_environment import TwinEnvironment
from twin.twin_model import TwinModel


class PressureSensor(Sensor):
    def __init__(self, name: str, direction: np.array, position: np.array):
        super().__init__(name)

        # normalised direction vector (0,0,1) is the same direction as the agent is facing)
        self.direction = direction
        self.position = position  # offset from agent position

    def update(self, twin: TwinModel, environment: TwinEnvironment):
        # TODO: add update functionality when we have a format for environments
        pass
