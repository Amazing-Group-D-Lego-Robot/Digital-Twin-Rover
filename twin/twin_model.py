from copy import deepcopy
from time import time_ns
import numpy as np
from scipy.spatial.transform import Rotation as R


class TwinModel:
    def __init__(self):
        # print("created new twin")

        # META INFO
        self.last_update_time = -1

        # POSITIONAL INFO
        # coordinate system is the ursina system
        #             y(up)
        #             |
        #             |
        # (forward) z |
        #           \ |
        #            \|
        #             *---------- x(right)
        self.forwards = np.array([0., 0., 1.])  # 3d unit vector pointing in our forwards direction

        self.pos = np.array([0., 0., 0.])  # 3d position vector
        self.vel = np.array([0., 0., 0.])  # 3d velocity vector
        self.acc = np.array([0., 0., 0.])  # 3d acceleration vector
        self.rot = np.array([0., 0., 0.])  # rotation in degrees about each axis

        # MOTORS
        self.motor_rots = [0, 0, 0, 0]  # motor rotation angles in degrees

        # SENSORS
        self.distance_sensor = 0  # number of mm to the nearest object ahead of the sensor

        # PROPERTIES
        self.wheel_diameter = 0.088  # diameter of the driving wheels in m
        self.movement_per_degree = (self.wheel_diameter * 3.141592654) / 360  # m of movement with 1 degree of turn

    def copy(self):
        # copy function for making predictions
        return deepcopy(self)

    def update(self, sensor_data, instruction, environment):
        # update state based upon truths and environment

        motor_deltas = [0, 0, 0, 0]

        if sensor_data is not None:
            # TODO: Update sensors when we have a structure for them
            motor_deltas[0] = sensor_data["A"] - self.motor_rots[0]
            motor_deltas[1] = sensor_data["B"] - self.motor_rots[1]
            motor_deltas[2] = sensor_data["C"] - self.motor_rots[2]

            self.motor_rots[0] = sensor_data["A"]
            self.motor_rots[1] = sensor_data["B"]
            self.motor_rots[2] = sensor_data["C"]

            self.rot[1] = sensor_data["Yaw"]
            r = R.from_euler("y", self.rot[1], degrees=True)
            self.forwards = r.apply(np.array([0., 0., 1.]))

        if instruction is not None:
            # TODO: Update state with instruction when we have a structure for them
            pass

        self.pos += self.forwards * (((motor_deltas[0] + motor_deltas[1]) / 2) * self.movement_per_degree)
        #print(self.forwards * (((motor_deltas[0] + motor_deltas[1]) / 2) * self.movement_per_degree))

    def predict_next(self, environment=None, instructions=None):
        # predict based upon a possible new instruction and simulated sensor data gathered
        # from the environment

        # start with the current state
        prediction = self.copy()

        # PREDICTION AREA

        # END OF PREDICTION AREA

        return prediction
