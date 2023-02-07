from twin.twin_model import TwinModel
from twin.twin_environment import TwinEnvironment


class WorldState:
    def __init__(self):
        # print("created new world state")

        self.environment = TwinEnvironment()

        def update_temp(twin):
            if not isinstance(twin, TwinModel):
                raise TypeError

            # PROPERTIES
            wheel_diameter = 0.088  # diameter of the driving wheels in m
            movement_per_degree = (wheel_diameter * 3.141592654) / 360  # m of movement with 1 degree of turn

            twin.rot[1] = twin.sensors["Yaw"]

            twin.pos += twin.get_forwards() * (
                        ((twin.sensor_deltas["A"] + twin.sensor_deltas["B"]) / 2) * movement_per_degree)

        self.twin = TwinModel(["A", "B", "C", "D", "Yaw", "Pitch", "Roll", "XAcc", "YAcc", "ZAcc", "Dist"])
        self.twin.add_update_function(update_temp)
