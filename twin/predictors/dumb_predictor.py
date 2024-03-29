import logging

import pandas as pd

from twin.twin_environment import TwinEnvironment
from twin.predictors.predictor import Predictor
from twin.predictors.errors.predictor_exceptions import MotorPortError

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
        self.state = None
        self.inst_splt = None

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

        # get final row of dataframe
        row = self.state.iloc[-1:]

        # get current wheel rotation
        current_pos = int(row["driving_motor_position"][-1:])

        # get angle of rotation in instruction
        angle_inst = int(self.inst_splt[3])

        # get new increments
        position_changer = _get_position_change_drive(current_pos, angle_inst)

        temp_row = row.copy()
        for inc_pos in position_changer:
            temp_row.at[0, "driving_motor_position"] = inc_pos
            row = pd.concat([row, temp_row], ignore_index=True)

        return row

    def _steering_prediction(self) -> pd.DataFrame:
        """
        Predict change based on steering position
        :return:pandas dataframe of predicted change
        """
        # TODO: Need to work out if Yaw and roll changes according to changing steering position (maybe safe to
        #  assume it doesn't)

        # change current steering motor position to change to new

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
