import numpy as np
import pandas as pd

from twin.predictors.predictor import Predictor


class DumbPredictor(Predictor):
    def __init__(self):
        super().__init__()
        # self.headers = ["time", "front_r", "front_g", "front_b", "front_intensity", "rear_r", "rear_g", "rear_b",
        #                 "rear_intensity", "distance_sensor", "accelerometer_x", "accelerometer_y", "accelerometer_z",
        #                 "yaw",
        #                 "pitch", "roll", "gyro_x", "gyro_y", "gyro_z", "steering_motor_position",
        #                 "driving_motor_position",
        #                 "force_sensor_newton"]
        #
        # self.last_df = pd.DataFrame(columns=self.headers)
        # self.last_df = pd.concat(pd.DataFrame(0, index=self.last_df.columns),self.last_df)
        # df2 = pd.DataFrame([[0] * df.shape[1]], columns=df.columns)

        # self.last_df = self.last_df.concat(, ignore_index=True)



    def predict_instruction(self, instruction: str, current_state: pd.DataFrame) -> pd.DataFrame:
        pass


if __name__ == "__main__":
    test = DumbPredictor()
