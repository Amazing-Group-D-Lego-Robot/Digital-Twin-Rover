import numpy as np

from twin.sensors.sensor import Sensor
from twin.twin_environment import TwinEnvironment
from twin.twin_model import TwinModel

from twin.sensors.errors.sensor_errors import AccelerationValueError


class AccelerationSensor(Sensor):
    def __init__(self, name: str, direction: np.array, position: np.array):
        super().__init__(name)

        # normalised direction vector (0,0,1) is the same direction as the agent is facing)
        self.direction = direction
        self.position = position  # offset from agent position
        self.value = np.array([0,0,0]) # same as normalised direction vector (I assume XYZ)

    def update(self, twin: TwinModel, environment: TwinEnvironment):
        # TODO: add update functionality when we have a format for environments
        pass

    def _update_value(self, value: np.array):
        """
        Update sensor value
        :param value: integer value for new acceleration measurement
        """
        if value.shape != (3,):
            raise AccelerationValueError(self.name,value)

        self.value = np.ndarray.copy(value)
