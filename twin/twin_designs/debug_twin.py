import numpy as np
import pandas as pd

from scipy.spatial.transform import Rotation as R

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
        self.wheel_diameter = 0.095  # diameter of the driving wheels in m
        self.movement_per_degree = (self.wheel_diameter * 3.141592654) / 360  # m of movement with 1 degree of turn

    def _update(self, sensor_data: dict, environment):
        self.rot[1] = self.sensors["Yaw"].value

        self.pos += self.get_forwards() * ((self.sensor_deltas["A"]) * self.movement_per_degree)


class DebugPredictor(Predictor):
    def __init__(self):
        # PROPERTIES
        self.wheel_diameter = 0.079  # diameter of the driving wheels in m
        self.movement_per_degree = (self.wheel_diameter * 3.141592654) / 360  # m of movement with 1 degree of turn
        self.degrees_yaw_change_per_degree_steer_angle_for_one_degree_drive = 0.0122

    def predict_instruction(self, environment: TwinEnvironment, instruction: str, current_state: pd.DataFrame) -> pd.DataFrame:
        def get_forwards(yaw):
            r = R.from_euler("xyz", np.array([0., yaw, 0.]), degrees=True)
            retv = r.apply(np.array([0., 0., 1.]))
            #print(retv)
            return retv

        ret = current_state.copy()

        if instruction.split(" ")[0] == "MOTOR":
            #print(int(instruction.split(" ")[3]))
            # move steer motor
            if instruction.split(" ")[1] == "A":
                ret["A"] += int(instruction.split(" ")[3])

            # drive forwards
            if instruction.split(" ")[1] == "C":
                # make a new row for each degree of movement
                for i in range(abs(int(instruction.split(" ")[3]))):
                    temp = ret.iloc[-1:].copy()

                    # update yaw so we turn
                    temp["Yaw"] = float(temp["Yaw"]) + ((float(temp["A"]) * self.degrees_yaw_change_per_degree_steer_angle_for_one_degree_drive) * (-1 if int(instruction.split(" ")[3]) < 0 else 1))

                    # move forwards
                    current_pos = np.array([float(temp["x_pos"]), float(temp["y_pos"]), float(temp["z_pos"])])

                    if int(instruction.split(" ")[3]) < 0:
                        current_pos -= get_forwards(float(temp["Yaw"])) * self.movement_per_degree
                    else:
                        current_pos += get_forwards(float(temp["Yaw"])) * self.movement_per_degree

                    # update values in dataframe
                    temp["C"] += -1 if int(instruction.split(" ")[3]) < 0 else 1
                    temp["x_pos"] = current_pos[0]
                    temp["y_pos"] = current_pos[1]
                    temp["z_pos"] = current_pos[2]
                    temp["y_rot"] = float(temp["Yaw"])

                    ret = pd.concat([ret, temp])

        return ret
