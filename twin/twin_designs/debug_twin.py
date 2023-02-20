import numpy as np

from twin.sensors.color_sensor import ColorSensor
from twin.sensors.sensor import Sensor
from twin.sensors.distance_sensor import DistanceSensor
from twin.sensors.pressure_sensor import PressureSensor
from twin.twin_model import TwinModel


# TODO: add more properties for things like size, display model, etc
class DebugTwinModel(TwinModel):
    def __init__(self):
        super().__init__()

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
            PressureSensor("Pres", np.array([0, 0, 1.]), np.array([0, 0, 0.]))
        ])

        # PROPERTIES
        self.wheel_diameter = 0.088  # diameter of the driving wheels in m
        self.movement_per_degree = (self.wheel_diameter * 3.141592654) / 360  # m of movement with 1 degree of turn

    def _update(self, sensor_data: dict, environment):
        self.rot[1] = self.sensors["Yaw"].value

        self.pos += self.get_forwards() * (
                ((self.sensor_deltas["A"] + self.sensor_deltas["B"]) / 2) * self.movement_per_degree)
