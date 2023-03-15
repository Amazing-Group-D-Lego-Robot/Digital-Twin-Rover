import numpy as np
import pandas as pd

from twin.predictors.predictor import Predictor
from twin.twin_model import TwinModel

__all__ = ["DumbTwinModel", "DumbPredictor"]


class DumbTwinModel(TwinModel):
    def __init__(self):
        super().__init__()

        # predictor
        self.predictor = DumbPredictor()

        # sensors


class DumbPredictor(Predictor):
    def __init__(self):
        super().__init__()
        self.instruction_switch = {
            "I:WAIT": self._return_current,
            "I:BEEP": self._return_current,
            "I:MOTOR": self._get_motor_prediction,
            "I:LIGHT_DISTANCE": self._return_current,
            "I:LIGHT_MATRIX": self._return_current,
            "I:LIGHT_STATUS": self._return_current,
        }
        self.state = None
        self.inst_splt = None

    def predict_instruction(self, instruction: str, current_state: pd.DataFrame) -> pd.DataFrame:
        self.state = current_state
        self.inst_splt = instruction.split(" ")  # splits instruction into [instruction, opcode(s) ...]
        inst_type = self.inst_splt[0]  # get just instruction type

        # retrieve correct function from dictionary
        decision_function = self.instruction_switch.get(inst_type)

        # get Dataframe result
        return decision_function()

    def _get_motor_prediction(self):
        """
        :return:
        """
        return self.state

    def _return_current(self) -> pd.DataFrame:
        """
        Dummy function that returns the current reading (for wait functions
        :return: Pandas dataframe that is the current state
        """
        return self.state
