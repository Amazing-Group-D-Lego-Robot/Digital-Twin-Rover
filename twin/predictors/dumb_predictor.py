import logging

import numpy as np
import pandas as pd

from twin.twin_environment import TwinEnvironment
from twin.predictors.predictor import Predictor
from twin.predictors.errors.predictor_exceptions import MotorPortError
from math import pi

__all__ = ["DumbPredictor"]

logger = logging.getLogger(__name__)


# TODO: Sort out the prediction in relation to the controller

class DumbPredictor(Predictor):
    def __init__(self, prev_inst=None, prev_state=None):
        super().__init__()

        # Possible list of instruction
        self.instruction_switch = {
            "I:WAIT": self._predict_wait,
            "I:BEEP": self._return_current,
            "I:MOTOR": self._get_motor_prediction,
            # TODO: Implement functions for these
            "I:LIGHT_DISTANCE": self._return_current,
            "I:LIGHT_MATRIX": self._return_current,
            "I:LIGHT_STATUS": self._return_current,
        }

        self.previous_state = prev_state
        self.previous_inst_splt = prev_inst

        # current state information
        self.state = None
        self.inst_splt = None

        # properties that aren't given in self.state
        self.properties = {
            "turning radius": None,
            "wheel diameter": np.array(0.088),
            "movement per degree": np.array((0.088 * pi) / 360),
            "velocity": np.array(0.1),  # m/s
            "sim_dt": np.array(0.1),  # dt for the simulation in seconds (not sure if needed)
            "lf": 0,  # f ront distance from center of mass of the car
            "lb": 0,  # Back distance from center of mass of the car
            "lw": 0,  # half of the width of the vehicle
            "prev_phi": 0,
            "elapsed_time": 0,
            "wheel_rotation_pos": np.array(0),
        }

    def predict_instruction(self, environment: TwinEnvironment, instruction: str,
                            current_state: pd.DataFrame) -> pd.DataFrame:
        """ Takes instruction and state(n) and predicts state(n + 1)
        :param environment:
        :param instruction: Instruction set instruction formatted as "I:INSTRUCTION OPCODE(S)"
        :param current_state: Dataframe of sensors from teh current state
        :return: the predicted instruction from the next state
        """
        logging.info(f"Starting predict instruction for {instruction}")
        if current_state is None:
            raise TypeError("current_state cannot be None")
        elif type(current_state) != pd.DataFrame:
            raise TypeError("The current state must be a dataframe", f"It is currently a {type(current_state)}")

        self.inst_splt = instruction.split(" ")  # splits instruction into [instruction, opcode(s) ...]
        inst_type = self.inst_splt[0]  # get just instruction type

        self.state = current_state
        # retrieve correct function from dictionary
        decision_function = self.instruction_switch.get(inst_type)

        # get Dataframe result
        result = decision_function()

        # keep last instruction REDUNDANT BUT COULD BE USEFUL
        self.previous_inst_splt = self.inst_splt

        # Makes sure wait conditions or blank predictions aren't added to the previous reading
        if current_state.shape[0] == 0:
            return result

        # Only useful for WAIT Command
        self.previous_state = self.state

        return result

    def _get_motor_prediction(self) -> pd.DataFrame:
        """
        Motor production handler
        :return: steering prediction dataframe
        """
        if self.inst_splt[1] == "C":
            logging.info("Predicting for Drive motor on port C")
            return self._drive_prediction()
        elif self.inst_splt[1] == "A":
            logging.info("Predicting for steering motor on port A")
            return self._steering_prediction()

        raise MotorPortError(self.inst_splt[1])

    def _drive_prediction(self) -> pd.DataFrame:
        """
        Predict statically change based on a motor drive command
        :return: pandas dataframe of predicted change
        """
        logger.info("Drive Prediction on instruction")
        logger.info(self.state.columns)

        ### OLD WAY
        # get final row of dataframe
        # row = self.state.iloc[-1:]
        #
        # # get current wheel rotation
        # current_pos = int(row["driving_motor_position"][-1:])
        #
        # # get angle of rotation in instruction
        # angle_inst = int(self.inst_splt[3])
        #
        # # get new increments
        # position_changer = _get_position_change_drive(current_pos, angle_inst)
        #
        # temp_row = row.copy()
        # for inc_pos in position_changer:
        #     temp_row.at[0, "driving_motor_position"] = inc_pos
        #     row = pd.concat([row, temp_row], ignore_index=True)

        curr_state = self.state.iloc[-1:]

        # get current z,x from the df
        curr_z = np.array(curr_state["z_pos"])
        curr_x = np.array(curr_state["x_pos"])
        curr_y_rot = np.array(curr_state["y_rot"])
        steering = np.deg2rad(np.array(curr_state["steering_pos"]))

        # total distance to travel m
        distance_to_travel = np.array(int(self.inst_splt[3])) * self.properties.get("movement per degree")
        logger.info(f"distance to travel in m is {distance_to_travel}")


        # velocity has to be assumed to be constant at 0.1 m/s
        velocity = self.properties.get("velocity")
        logger.info(f"Velocity is {velocity}")
        # TODO: calculate velocity as a component of z and x vel + y rotation and steering angle\
        # assume y is from the axis of z i.e. that y axis rotation is theta_z

        # since velocity is 0.1 m/s we want to calculate the change in z and y in 0.1s, so we get a df value every
        # 0.01 second
        dz = None
        dx = None

        dz = np.arccos(velocity/0.1)


        # get the required properties

        new_state = curr_state.copy(deep = True)

        return curr_state

    def update_zx_drive(self):
        """Assigns new emd xyz coordinates based on current direction"""

        # FOR NOW ASSUME ONLY FORWARDS OR BACKWARDS
        # TODO: Implement forwards and backwards movement based off rover direction
        # TODO: Implement moving in none stright line whilst wheels are at an angle

        ### Plan
        # We want to workout the change in x and y based on the motor command issued

        # Given the angle, current position,

        # this will be an arc depending on turning angle
        distance_to_move = self.properties.get("movement per degree") * int(self.inst_splt[3])
        rotation = self.properties.get("rotation")
        # distance to move an be considered an arc
        # so we have arc length, and inital angle workout ending vector

        # Get properties from dictionary


        vel = self.properties.get("velocity")
        steering = np.deg2rad(self.properties.get("yaw"))

        lb = self.properties.get("lb")
        lf = self.properties.get("lf")

        prev_phi = self.properties.get("prev_phi")

        # get time
        time = abs(distance_to_move / vel)

        # calculate heading of the vehicle
        beta = np.arctan(lb*np.tan(steering)/(lb + lf))
        prev_phi = self.properties.get("prev_phi")
        sim_dt = self.properties.get("sim_dt")
        phi = prev_phi + vel * sim_dt * np.cos(beta) * np.tan(steering)/ (lb * lf)

        # calculate new z and z (x and y respectively)



    def _steering_prediction(self) -> pd.DataFrame:
        """
        Predict change based on steering position
        :return:pandas dataframe of predicted change
        """
        # TODO: Need to work out if Yaw and roll changes according to changing steering position (maybe safe to
        #  assume it doesn't)

        # change current steering motor position to change to new
        logger.info(f"Steering prediction rotation angle {self.inst_splt[3]} {self.inst_splt[1]}")

        # get last row
        row = self.state.iloc[-1:]

        angle_inst = int(self.inst_splt[3])
        current_pos = int(row["steering_motor_position"][-1:])
        new_pos = current_pos + angle_inst

        position_changer = _get_position_change_steering(current_pos, new_pos)

        temp_row = row[-1:].copy()
        for inc_pos in position_changer:
            temp_row["steering_motor_position"] = inc_pos
            row = pd.concat([row, temp_row], ignore_index=True)

        # change steering position to new steering position

        return row.iloc[1:]

    def _return_current(self) -> pd.DataFrame:
        """
        Handles instructions where no change in state takes place e.g. BEEP
        :return : Pandas dataframe that is the current state
        """
        logger.info("returning current state")
        return self.state

    def _predict_wait(self) -> pd.DataFrame:
        """
        Since wait returns a null dataframe we assume
        :return: dataframe of the previous state or if prev state is none the current state
        """

        # in the event there is no other option we return the empty wait dataframe
        if self.previous_state is None:
            raise TypeError("The previous state cannot be None it must be of type pd.DataFrame")

        logger.info("returning previous state for wait")

        return self.previous_state


def _get_position_change_drive(current_pos, angle_inst) -> list:
    """
    Get change in driving motors
    :param current_pos: the current position of the motor
    :param angle_inst: the amount of degrees to turn it
    :return: list of increments value of each list 0 <= val < 360
    """

    # Get increments for position change
    if angle_inst < 0:  # if angle is a negative angle
        position_changer = [(current_pos + i) % 360 for i in range(-1, angle_inst - 1, -1)]
    else:  # if angle is positive
        position_changer = [(current_pos + i) % 360 for i in range(1, angle_inst + 1)]

    return position_changer


def _get_position_change_steering(current, new) -> list:
    """
    Gets change in steering position as list of increments
    :param current: old degrees
    :param new: new degrees
    :return: list of increments
    """

    # given a steering position that goes backwards
    if current > new:
        position_changer = [i for i in range(current, new - 1, -1)]
    else:
        position_changer = [i for i in range(current, new + 1)]

    return position_changer

def _get_radians(angle:np.array)->np.array:
    """Given angle in degrees returns radians"""
    return