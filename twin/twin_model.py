from copy import deepcopy
from time import time_ns
import numpy as np
from scipy.spatial.transform import Rotation as R


class TwinModel:
    def __init__(self, sensors=None):
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

        self.pos = np.array([0., 0., 0.])  # 3d position vector
        self.vel = np.array([0., 0., 0.])  # 3d velocity vector
        self.acc = np.array([0., 0., 0.])  # 3d acceleration vector
        self.rot = np.array([0., 0., 0.])  # rotation in degrees about each axis

        if sensors is not None:
            self.sensors = {name: 0 for name in sensors}  # dict of sensor name value pairs
            self.sensor_deltas = {name: 0 for name in sensors}  # dict of sensor name value pairs
        else:
            self.sensors = dict()
            self.sensor_deltas = dict()

        # Values that need to be derived / set at update:
        #   - self.pos
        #   - self.vel
        #   - self.acc
        #   - self.rot

        self.update_funcs = []  # list of functions to execute every update step

    def add_update_function(self, function):
        self.update_funcs.append(function)

    def get_forwards(self):
        r = R.from_euler("xyz", self.rot, degrees=True)
        return r.apply(np.array([0., 0., 1.]))

    def copy(self):
        # copy function for making predictions
        return deepcopy(self)

    def update(self, sensor_data: dict, instruction, environment):
        # update state based upon truths and environment
        for key, item in sensor_data.items():
            if key in self.sensors:
                self.sensor_deltas[key] = sensor_data[key] - self.sensors[key]
                self.sensors[key] = sensor_data[key]

        for update_func in self.update_funcs:
            update_func(self)

        if instruction is not None:
            # TODO: Update state with instruction when we have a structure for them
            pass

    def predict_next(self, environment=None, instructions=None):
        # predict based upon a possible new instruction and simulated sensor data gathered
        # from the environment

        # start with the current state
        prediction = self.copy()

        # PREDICTION AREA

        # END OF PREDICTION AREA

        return prediction
