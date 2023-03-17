import numpy as np

from twin.twin_model import TwinModel

from twin.sensors.sensor import Sensor
from twin.sensors.force_sensor import ForceSensor
from twin.sensors.distance_sensor import DistanceSensor
from twin.sensors.gyro_sensor import GyroSensor
from twin.sensors.acceleration_sensor import AccelerationSensor
from twin.sensors.color_sensor import ColorSensor
from twin.predictors.dumb_predictor import DumbPredictor

__all__ = ["DumbTwinModel"]


class DumbTwinModel(TwinModel):
    def __init__(self):
        super().__init__()

        # predictor
        self.predictor = DumbPredictor()

        sensors = [
            ColorSensor("FrontRGB", direction=np.array([0, 0, 1]), position=np.array([0, 0, 0])),
            # TODO: Change bottom RGB direction to be correct as well as position
            ColorSensor("BottomRGB", direction=np.array([0, 1, 0]), position=np.array([0, 0, 0])),

            # TODO: Check if this is Rear Distance is correct direction and position
            DistanceSensor("RearDist", direction=np.array([0, 0, 1]), position=np.array([0, 0, 0])),

            # TODO: Check if this is Front Force is correct direction and position
            ForceSensor("FrontForce", direction=np.array([0, 0, 1]), position=np.array([0, 0, 0])),

            # Assuming middle of spike is where the acceleration sensor and gyro sensor is
            AccelerationSensor("Acc", direction=np.array([0, 0, 1]), position=np.array([0, 0, 0])),
            GyroSensor("Gyro", direction=np.array([0, 0, 1]), position=np.array([0, 0, 0])),

            Sensor("pitch"),
            Sensor("roll"),
            Sensor("yaw")


        ]

        self.set_sensors(sensors)

