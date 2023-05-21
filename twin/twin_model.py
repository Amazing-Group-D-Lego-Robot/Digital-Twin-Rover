import logging

from copy import deepcopy
from time import time_ns
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R

from twin.predictors.predictor import Predictor
from twin.predictors.dumb_predictor import DumbPredictor
from twin.twin_environment import TwinEnvironment

logger = logging.getLogger(__name__)

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

        self.predictor = DumbPredictor()

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

    def get_current_state_as_df(self) -> pd.DataFrame:
        """
        Gets current sensor values and returns them as a pandas dataframe
        """
        # TODO: update this to reflect the new sensor values
        ret = {key: [self.sensors[key].value] for key in self.sensors.keys()}
        ret.update({
            "x_pos": [self.pos.copy()[0]],
            "x_vel": [self.vel.copy()[0]],
            "x_acc": [self.acc.copy()[0]],
            "x_rot": [self.rot.copy()[0]],
            "y_pos": [self.pos.copy()[0]],
            "y_vel": [self.vel.copy()[0]],
            "y_acc": [self.acc.copy()[0]],
            "y_rot": [self.rot.copy()[0]],
            "z_pos": [self.pos.copy()[0]],
            "z_vel": [self.vel.copy()[0]],
            "z_acc": [self.acc.copy()[0]],
            "z_rot": [self.rot.copy()[0]]
        })
        return pd.DataFrame.from_dict(ret)

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

    def update_from_prediction(self, prediction, cols):
        for col in cols:
            if col not in ["x_pos", "x_vel", "x_acc", "x_rot", "y_pos", "y_vel", "y_acc", "y_rot", "z_pos", "z_vel",
                           "z_acc", "z_rot", "Unnamed: 0"]:
                self.sensors[col].value = prediction[col]

        self.pos = np.array([prediction["x_pos"], prediction["y_pos"], prediction["z_pos"]])
        self.vel = np.array([prediction["x_vel"], prediction["y_vel"], prediction["z_vel"]])
        self.acc = np.array([prediction["x_acc"], prediction["y_acc"], prediction["z_acc"]])
        self.rot = np.array([prediction["x_rot"], prediction["y_rot"], prediction["z_rot"]])

    def predict_next(self, environment=None, instructions=None):
        # TODO: use the environment in the prediction

        # start with the current state
        prediction = self.get_current_state_as_df()  # updated each instruction

        # PREDICTION AREA
        if self.predictor is not None:
            # for each instruction, predict 100 states with the last state in "prediction" acting as the current_state
            # then append the predictions to the end of "prediction"
            for instruction in instructions:
                prediction = \
                    pd.concat([prediction, self.predictor.predict_instruction(environment, instruction, prediction.iloc[-1:])])
        # END OF PREDICTION AREA

        return prediction
