import numpy as np

from twin.sensors.sensor import Sensor
from twin.twin_environment import TwinEnvironment
from twin.twin_model import TwinModel

from twin.sensors.errors.sensor_errors import GyroValueError


class GyroSensor(Sensor):
    def __init__(self, name: str, direction: np.array, position: np.array):
        super().__init__(name)

        # normalised direction vector (0,0,1) is the same direction as the agent is facing)
        self.direction = direction
        self.position = position  # offset from agent position

    def update(self, twin: TwinModel, environment: TwinEnvironment):
        # TODO: add update functionality when we have a format for environments
        pass

    def _update_value(self, value: np.array):
        """
        Update sensor value
        :param value: integer value for new gyro
        """
        if value.shape != (3,):
            raise GyroValueError(self.name, value)

        self.value = value
