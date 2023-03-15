import numpy as np
import pandas as pd

from twin.predictors.predictor import Predictor
from twin.twin_model import TwinModel

from twin.sensors.sensor import Sensor
from twin.sensors.color_sensor import ColorSensor
from twin.sensors.distance_sensor import DistanceSensor
from twin.sensors.pressure_sensor import PressureSensor

__all__ = ["DumbTwinModel", "DumbPredictor"]


class DumbTwinModel(TwinModel):
    def __init__(self):
        super().__init__()

        # predictor
        self.predictor = DumbPredictor()

        # sensors

        sensors = [
            # Sensors for the spike
            Sensor("Yaw"),
            Sensor(""),

            # Sensors that are from IO e.g. ports
            ColorSensor("Front_RGB"),
            ColorSensor("Bottom_RGB"),
        ]

        self.set_sensors(sensors)


class DumbPredictor(Predictor):
    def __init__(self, prev_inst=None, prev_state=None):
        super().__init__()
        self.instruction_switch = {
            "I:WAIT": self._predict_wait,
            "I:BEEP": self._return_current,
            "I:MOTOR": self._get_motor_prediction,
            "I:LIGHT_DISTANCE": self._return_current,
            "I:LIGHT_MATRIX": self._return_current,
            "I:LIGHT_STATUS": self._return_current,
        }
        self.previous_state = prev_state
        self.previous_inst_splt = prev_inst
        self.state = None
        self.inst_splt = None

    def predict_instruction(self, instruction: str, current_state: pd.DataFrame) -> pd.DataFrame:
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

        # currently redundant but might be useful for some functions e.g. retrieving previous yaw
        if current_state.shape[0] == 0:
            return result

        self.previous_state = self.state
        self.previous_inst_splt = self.inst_splt

        return result

    def _get_motor_prediction(self) -> pd.DataFrame:
        """
        :return :
        """
        return self.state

    def _return_current(self) -> pd.DataFrame:
        """
        Handles instructions where no change in state takes place e.g. BEEP
        :return : Pandas dataframe that is the current state
        """
        return self.state

    def _predict_wait(self) -> pd.DataFrame:
        """
        Since wait returns a null dataframe we assume
        :return: dataframe of the previous state or if prev state is none the current state
        """

        # in the event there is no other option we return the empty wait dataframe
        # TODO: Do I want it to do this or raise an Error?
        if self.previous_state is None:
            return self.state

        return self.previous_state

