import numpy as np
import pandas as pd

from twin.twin_model import TwinModel

from twin.predictors.basic_predictor import BasicPredictor


class BasicTwinModel(TwinModel):
    def __init__(self):
        super().__init__()

        self.predictor = BasicPredictor()

        sensors = [
            # TODO: Put appropriate sensors in here
        ]

        self.set_sensors(sensors)

        self.wheel_diameter = 0.088

    def _update(self, sensor_data: dict, environment):
        pass
