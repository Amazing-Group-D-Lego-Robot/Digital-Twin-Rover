import numpy as np
import pandas as pd

from twin.predictors.predictor import Predictor
from twin.sensors.color_sensor import ColorSensor
from twin.sensors.sensor import Sensor
from twin.sensors.distance_sensor import DistanceSensor
from twin.sensors.force_sensor import ForceSensor
from twin.twin_environment import TwinEnvironment
from twin.twin_model import TwinModel


# TODO: add more properties for things like size, display model, etc
class DebugTwinModel(TwinModel):
    def __init__(self):
        super().__init__()

        # PREDICTOR
        self.predictor = DebugPredictor()

        # SENSORS
        self.set_sensors([
            Sensor("A"),
            Sensor("B"),
            Sensor("C"),
            Sensor("D"),
            Sensor("Yaw"),
            Sensor("Pitch"),
            Sensor("Roll"),
            Sensor("XAcc"),
            Sensor("YAcc"),
            Sensor("ZAcc"),
            DistanceSensor("Dist", np.array([0, 0, 1.]), np.array([0, 0, 0.])),
            ColorSensor("Col", np.array([0, 0, 1.]), np.array([0, 0, 0.])),
            ForceSensor("Pres", np.array([0, 0, 1.]), np.array([0, 0, 0.]))
        ])

        # PROPERTIES
        self.wheel_diameter = 0.088  # diameter of the driving wheels in m
        self.movement_per_degree = (self.wheel_diameter * 3.141592654) / 360  # m of movement with 1 degree of turn

    def _update(self, sensor_data: dict, environment):
        self.rot[1] = self.sensors["Yaw"].value

        self.pos += self.get_forwards() * (
                ((self.sensor_deltas["A"] + self.sensor_deltas["B"]) / 2) * self.movement_per_degree)


class DebugPredictor(Predictor):
    def __init__(self):
        # memory and storage goes here
        pass

    def predict_instruction(self, environment: TwinEnvironment, instruction: str, current_state: pd.DataFrame) -> pd.DataFrame:
        ret = current_state.copy()
        ret["z_pos"] += 0.01
        ret["A"] += 0.1

        for i in range(99):
            temp = ret.iloc[-1:].copy()
            temp["z_pos"] += 0.01
            temp["A"] += 0.1
            ret = pd.concat([ret, temp])

        return ret
