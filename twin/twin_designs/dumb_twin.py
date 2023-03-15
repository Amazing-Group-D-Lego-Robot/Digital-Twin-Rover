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


def _return_current(*args) -> pd.DataFrame:
    """
    Dummy function that returns the current reading
    :param inst_lst:
    :param current_state:
    :return:
    """
    return args[0]


class DumbPredictor(Predictor):
    def __init__(self):
        super().__init__()
        self.instruction_switch = {
            "I:WAIT": _return_current,
            "I:BEEP": _return_current,
            "I:MOTOR": _return_current,
            "I:LIGHT_DISTANCE": _return_current,
            "I:LIGHT_MATRIX": _return_current,
            "I:LIGHT_STATUS": _return_current,
        }
        self.last_inst = None
        self.last_state = None

    def predict_instruction(self, instruction: str, current_state: pd.DataFrame) -> pd.DataFrame:
        inst_lst = instruction.split(" ")  # splits instruction into [instruction, opcode(s) ...]
        inst_type = inst_lst[0]  # get just instruction type

        decision_function = self.instruction_switch.get(inst_type)

        return decision_function(inst_lst, current_state)
