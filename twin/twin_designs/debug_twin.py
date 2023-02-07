from twin.twin_model import TwinModel


class DebugTwinModel(TwinModel):
    def __init__(self):
        super().__init__()

        # SENSORS
        self.set_sensors(["A", "B", "C", "D", "Yaw", "Pitch", "Roll", "XAcc", "YAcc", "ZAcc", "Dist"])

        # PROPERTIES
        self.wheel_diameter = 0.088  # diameter of the driving wheels in m
        self.movement_per_degree = (self.wheel_diameter * 3.141592654) / 360  # m of movement with 1 degree of turn

    def update(self, sensor_data: dict, instruction, environment):
        super().update(sensor_data, instruction, environment)

        self.rot[1] = self.sensors["Yaw"]

        self.pos += self.get_forwards() * (
                ((self.sensor_deltas["A"] + self.sensor_deltas["B"]) / 2) * self.movement_per_degree)
