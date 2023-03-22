import numpy as np
import pandas as pd

from twin.twin_model import TwinModel

from twin.sensors.sensor import Sensor
from twin.sensors.force_sensor import ForceSensor
from twin.sensors.distance_sensor import DistanceSensor
from twin.sensors.gyro_sensor import GyroSensor
from twin.sensors.acceleration_sensor import AccelerationSensor
from twin.sensors.color_sensor import ColorSensor
from twin.predictors.dumb_predictor import DumbPredictor

from math import pi

__all__ = ["DumbTwinModel"]


class DumbTwinModel(TwinModel):
    def __init__(self):
        super().__init__()

        # predictor
        self.predictor = DumbPredictor()

        # Sensors Modelled as if on rover
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

            # General sensors -> sensors that only take on integer value as input
            Sensor("pitch"),
            Sensor("roll"),
            Sensor("yaw"),
            Sensor("steering_pos"),
            Sensor("wheel_rotation_pos"),
        ]

        self.set_sensors(sensors)

        # Useful properties
        self.wheel_diameter = 0.088  # diameter in m
        self.movement_per_degree = (self.wheel_diameter * pi) / 360  # movement in m per degree

    def _update(self, instruction_step: dict, environment) -> pd.DataFrame:
        """
        Takes in instruction_step dictionary and returns the predicted next state
        :param instruction_step:
        :param environment:
        :return: predicted next state
        """
        instruction = instruction_step.get("instruction")
        current_state = instruction_step.get("measurrements")
        updated_state = self.predictor.predict_instruction(environment, instruction, current_state)

        return updated_state
