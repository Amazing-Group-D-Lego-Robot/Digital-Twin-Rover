from twin.sensors.color_sensor import ColorSensor
from twin.sensors.default_sensor import DefaultSensor
from twin.sensors.distance_sensor import DistanceSensor
from twin.sensors.pressure_sensor import PressureSensor
from twin.twin_model import TwinModel


class DebugTwinModel(TwinModel):
    def __init__(self):
        super().__init__()

        # SENSORS
        self.set_sensors([
            DefaultSensor("A"),
            DefaultSensor("B"),
            DefaultSensor("C"),
            DefaultSensor("D"),
            DefaultSensor("Yaw"),
            DefaultSensor("Pitch"),
            DefaultSensor("Roll"),
            DefaultSensor("XAcc"),
            DefaultSensor("YAcc"),
            DefaultSensor("ZAcc"),
            DistanceSensor("Dist"),
            ColorSensor("Col"),
            PressureSensor("Pres")
        ])

        # PROPERTIES
        self.wheel_diameter = 0.088  # diameter of the driving wheels in m
        self.movement_per_degree = (self.wheel_diameter * 3.141592654) / 360  # m of movement with 1 degree of turn
        # TODO: add more properties for things like size, display model, sensor position, sensor properties, etc

    def _update(self, sensor_data: dict, instruction, environment):
        self.rot[1] = self.sensors["Yaw"].value

        self.pos += self.get_forwards() * (
                ((self.sensor_deltas["A"] + self.sensor_deltas["B"]) / 2) * self.movement_per_degree)
