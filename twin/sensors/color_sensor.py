import numpy as np

from twin.sensors.sensor import Sensor
from twin.twin_environment import TwinEnvironment
from twin.twin_model import TwinModel
from twin.sensors.errors.sensor_errors import RGBSensorValueError


class ColorSensor(Sensor):
    def __init__(self, name: str, direction: np.array, position: np.array):
        super().__init__(name)

        # normalised direction vector (0,0,1) is the same direction as the agent is facing)
        self.direction = direction
        self.position = position  # offset from agent position
        self.value = np.array([0, 0, 0, 0])  # RGB Values and intensity for colour sensor

    def update(self, twin: TwinModel, environment: TwinEnvironment):
        # TODO: add update functionality when we have a format for environments
        pass

    def _update_value(self, rgbi_vals: np.array):
        """
        Update rgb & intensity values
        :param rgbi_vals: (4,) numpy array contains [R,G,B,intensity] as np
        """
        if (shape := rgbi_vals.shape) != (4,):
            raise RGBSensorValueError(self.name, shape)

        self.value = rgbi_vals
