from copy import deepcopy
from time import time_ns
import numpy as np
from scipy.spatial.transform import Rotation as R

from twin.twin_environment import TwinEnvironment


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

        self.pos = np.array([0., 0., 0.])  # 3d position vector
        self.vel = np.array([0., 0., 0.])  # 3d velocity vector
        self.acc = np.array([0., 0., 0.])  # 3d acceleration vector
        self.rot = np.array([0., 0., 0.])  # rotation in degrees about each axis

        # Values that need to be derived / set at update:
        #   - self.pos
        #   - self.vel
        #   - self.acc
        #   - self.rot

        self.sensors = dict()  # dict of sensors
        self.sensor_deltas = dict()  # dict of sensor changes from last update

        self.memory = dict()
        self.current_instruction = None
        self.memory_buffer = []

    def set_sensors(self, sensors: list):
        self.sensors = {sensor.name: sensor for sensor in sensors}
        self.sensor_deltas = {sensor.name: 0 for sensor in sensors}

    def get_forwards(self):
        r = R.from_euler("xyz", self.rot, degrees=True)
        return r.apply(np.array([0., 0., 1.]))

    def copy(self):
        # copy function for making predictions
        return deepcopy(self)

    def get_sensors_and_properties(self):
        ret = {key: self.sensors[key].value for key in self.sensors.keys()}
        ret.update({
            "_pos": self.pos.copy(),
            "_vel": self.vel.copy(),
            "_acc": self.acc.copy(),
            "_rot": self.rot.copy()
        })
        return ret

    def change_instruction(self, instruction: str):
        # TODO: add normalisation for instruction length / data
        if self.current_instruction is not None:
            if self.current_instruction in self.memory:
                self.memory[self.current_instruction].append(self.memory_buffer)
            else:
                self.memory[self.current_instruction] = [self.memory_buffer]

        self.current_instruction = instruction
        self.memory_buffer = []

    def _update(self, sensor_data: dict, environment: TwinEnvironment):
        """
        To be overwritten by child classes

        :param sensor_data:
        :param environment:
        :return: None
        """
        pass

    def update(self, sensor_data, environment: TwinEnvironment):
        # update state based upon truths and environment
        for key, item in sensor_data.items():
            if key in self.sensors:
                self.sensor_deltas[key] = sensor_data[key] - self.sensors[key].value
                self.sensors[key].value = sensor_data[key]

        self._update(sensor_data, environment)

        if self.current_instruction is not None:
            self.memory_buffer.append(sensor_data)

    def predict_next(self, environment=None, instructions=None):
        # start with the current state
        prediction = self.copy()

        # PREDICTION AREA
        # TODO: do something here
        # END OF PREDICTION AREA

        return prediction
