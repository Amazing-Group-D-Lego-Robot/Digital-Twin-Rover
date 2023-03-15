import numpy as np
import pandas as pd

from twin.predictors.predictor import Predictor
from twin.twin_model import TwinModel

class DumbTwinModel(TwinModel):
    def __init__(self):
        super().__init__()

        # predictor
        self.predictor = DumbPredictor()

        #sensors

class DumbPredictor(Predictor):
    def __init__(self):
        super().__init__()



    def predict_instruction(self, instruction: str, current_state: pd.DataFrame) -> pd.DataFrame:
        pass


if __name__ == "__main__":
    test = DumbPredictor()
