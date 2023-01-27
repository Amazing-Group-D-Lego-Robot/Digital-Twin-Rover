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
        self.motor_speeds = [0, 0, 0, 0]  # motor speed in range [0, 1]
        self.motor_rots = [0, 0, 0, 0]  # motor rotation angles in degrees

        # SENSORS
        self.distance_sensor = 0  # number of mm to the nearest object ahead of the sensor

        # PROPERTIES
        self.wheel_diameter = 0.088  # diameter of the driving wheels in m
        self.movement_per_degree = (self.wheel_diameter * 3.141592654) / 360  # m of movement with 1 degree of turn

    def copy(self):
        # copy function for making predictions
        return deepcopy(self)

    def update(self, sensor_data, instruction, environment, tdelta=None):
        # update state based upon truths and environment

        if sensor_data is not None:
            # TODO: Update sensors when we have a structure for them
            pass

        if instruction is not None:
            # TODO: Update state with instruction when we have a structure for them
            pass

    def predict_next(self, n=1, environment=None, instruction=None):
        # predict based upon a possible new instruction and simulated sensor data gathered
        # from the environment

        def predict_step(_n, current, futures, _environment, _instruction):
            if not isinstance(current, TwinModel):
                raise TypeError()

            # start with the current state
            prediction = current.copy()

            # PREDICTION AREA

            # END OF PREDICTION AREA

            # append the new prediction to our list of future states
            futures.append(prediction)

            # exit condition
            if _n == 1:
                return futures
            else:
                return predict_step(_n - 1, futures[-1], futures, _environment, _instruction)

        return predict_step(n, self, [], environment, instruction)
