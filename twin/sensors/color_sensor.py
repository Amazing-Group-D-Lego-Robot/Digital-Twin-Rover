import numpy as np

from twin.sensors.sensor import Sensor
from twin.twin_environment import TwinEnvironment
from twin.twin_model import TwinModel
from twin.sensors.errors.SensorErrors import RGBValueSizeError


class ColorSensor(Sensor):
    def __init__(self, name: str, direction: np.array, position: np.array):
        super().__init__(name)

        # normalised direction vector (0,0,1) is the same direction as the agent is facing)
        self.direction = direction
        self.position = position  # offset from agent position
        self.rgb_value = np.array([0, 0, 0, 0])  # RGB Values and intensity for colour sensor

    def update(self, twin: TwinModel, environment: TwinEnvironment):
        # TODO: add update functionality when we have a format for environments
        pass

    def _update_value(self, rgb_vals: np.array):
        """
        Update rgb values
        :param rgb_vals: 1 x 4 array contain [[R,G,B,intensity]] as np array
        """
        if np.shape(1,4):
            raise RGBValueSizeError(np.shape, type(rgb_vals))

        self.rgb_value = np.ndarray.copy(rgb_vals)
