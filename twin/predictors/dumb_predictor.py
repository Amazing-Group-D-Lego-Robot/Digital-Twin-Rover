import logging
import math

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
            "wheel diameter": np.array(0.079),
            "movement per degree": np.array((0.079 * pi) / 360, dtype=np.longdouble),
            "velocity": np.array(0.1),  # m/s
            "sim_dt": np.array(0.01),  # dt for the simulation in seconds (not sure if needed)
            "lf": 0,  # front distance from center of mass of the car
            "lb": 0,  # Back distance from center of mass of the car
            "lw": 0,  # half of the width of the vehicle
            "prev_phi": 0,
            "elapsed_time": 0,
            "wheel_rotation_pos": np.array(0),
            "phi": 0,

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

        curr_state = self.state.iloc[-1:]
        steering = np.array(curr_state["steering_pos"])
        logger.info(f"Steering in degrees {curr_state['steering_pos']} \t steering in radians {steering}")

        # get the turning radius

        if (steering == 0).all():
            logger.info("Straight line prediction (0 degrees of steering)")
            new_prediction = self.drive_predict_no_steering(curr_state)
        else:
            logger.info(f"Predicting for steering angle of {steering}")
            new_prediction = self.drive_predict_steering(curr_state=curr_state, steering_angle=steering)

        logger.info("End of steering prediction")
        return new_prediction

    def drive_predict_no_steering(self, curr_state):
        distance_to_travel = self.properties.get("movement per degree") * np.array(float(self.inst_splt[3]),
                                                                                   dtype=np.longdouble)
        logger.info(f"Distance to travel: {distance_to_travel} (no steering)")
        y_rot = np.deg2rad(curr_state["y_rot"])

        vel = self.properties.get("velocity")

        # orientation in terms of cartesian cordinates
        if (y_rot > 1.5 * np.pi).all():
            # +ve z, -ve x
            new_rot = y_rot - (1.5 * np.pi)
            z_dist = distance_to_travel * np.cos(new_rot)
            x_dist = -distance_to_travel * np.sin(new_rot)
        elif (y_rot > np.pi).all():
            # negative z axis, negative z
            new_rot = y_rot - np.pi
            z_dist = -(distance_to_travel) * np.cos(new_rot)
            x_dist = -(distance_to_travel) * np.sin(new_rot)
        elif (y_rot > 0.5 * np.pi).all():
            # negative z axis, positive x
            new_rot = y_rot - (0.5 * np.pi)
            z_dist = -(distance_to_travel * np.cos(new_rot))
            x_dist = distance_to_travel * np.sin(new_rot)
        else:
            z_dist = distance_to_travel * np.cos(y_rot)
            x_dist = distance_to_travel * np.sin(y_rot)

        increment_z_distance = (z_dist / 100)[0]
        increment_x_distance = (x_dist / 100)[0]

        logger.info(f"increment z :{increment_z_distance}\n increment x: {increment_x_distance}")

        curr_z = curr_state["z_pos"].iloc[-1:]
        curr_x = curr_state["x_pos"].iloc[-1:]

        new_z = curr_z.copy()
        new_x = curr_x.copy()
        new_y = y_rot.copy()

        for i in range(1, 101):
            curr_z += increment_z_distance
            new_z = np.vstack((new_z, curr_z))

            curr_x += increment_x_distance
            new_x = np.vstack((new_x, curr_x))

            new_y = np.vstack((new_y, y_rot))

        logger.info(f"new_z {new_z}")
        logger.info(f"new_x {new_x}")

        temp_state = curr_state.iloc[-1:]

        new_state = pd.DataFrame(columns=curr_state.columns)
        for i in range(0, 101):
            temp_state["z_pos"] = new_z[i]
            temp_state["x_pos"] = new_x[i]
            new_state = new_state.append(temp_state, ignore_index=True)

        return new_state

    def drive_predict_steering(self, curr_state, steering_angle):
        distance_to_travel = self.properties.get("movement per degree") * np.array(float(self.inst_splt[3]),
                                                                                   dtype=np.longdouble)

        steering_angle = np.deg2rad(steering_angle)

        # Paulwessen's properties
        lf = self.properties.get("lf")
        lb = self.properties.get("lb")
        lw = self.properties.get("lw")
        v = self.properties.get("velocity")
        sim_dt = self.properties.get("sim_dt")
        prev_phi = self.properties.get("phi") # get yaw from dataframe

        # Calculate heading of the vehicle.
        beta = np.arctan(lb * np.tan(steering_angle) / (lb + lf))

        new_z = curr_state["z_pos"].iloc[-1:]
        new_x = curr_state["x_pos"].iloc[-1:]
        y_rot = np.deg2rad(curr_state["y_rot"].iloc[-1:])

        x_changes = []
        z_changes = []
        yaw_changes = []
        prev_phi = self.properties.get["phi"] #change to yaw offset?
        dist_left = distance_to_travel
        for i in range(math.ceil(distance_to_travel / (v * sim_dt))):
            if dist_left - v*sim_dt <= 0:
                sim_dt = dist_left / v
                dist_left = 0
            else:
                dist_left -= v*sim_dt

            # Calculate vehicle's position.
            phi = prev_phi + v * sim_dt * np.cos(beta) * np.tan(steering_angle) / (lb + lf)
            new_x = new_x + v * sim_dt * np.cos(beta + phi)  # may actually be x (x-axis in 2d)
            new_z = new_z + v * sim_dt * np.sin(beta + phi)  # may actually be z (y-axis in 2d) (i think)
            yaw_changes.append(phi)
            x_changes.append(new_x)
            z_changes.append(new_z)

        self.properties["phi"] = phi


        temp_state = curr_state.iloc[-1:]

        new_state = pd.DataFrame(columns=curr_state.columns)
        for i in range(len(new_x)):
            temp_state["z_pos"] = z_changes[i]
            temp_state["x_pos"] = x_changes[i]
            temp_state["y_rot"] = yaw_changes[i]
            new_state = new_state.append(temp_state, ignore_index=True)


        return new_state

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
