from copy import deepcopy


class TwinModel:
    def __init__(self):
        # print("created new twin")

        self.x_pos = 0  # relative x-axis displacement from start position
        self.y_pos = 0  # relative y-axis displacement from start position
        self.z_pos = 0  # relative z-axis displacement from start position

        self.x_vel = 0  # x-axis velocity from start position
        self.y_vel = 0  # y-axis velocity from start position
        self.z_vel = 0  # z-axis velocity from start position

        self.x_rot = 0  # x-axis rotation from upright
        self.y_rot = 0  # y-axis rotation from upright
        self.z_rot = 0  # z-axis rotation from upright

        # TODO: add sensor information to the twin storage when available

    def copy(self):
        # copy function for making predictions
        return deepcopy(self)

    def update(self, sensor_data, instruction):
        # update state based upon truths
        pass

    def predict_next(self, n=1, environment=None, instruction=None):
        # predict based upon a possible new instruction and simulated sensor data gathered
        # from the environment

        def predict_step(_n, current, futures, _environment, _instruction):
            if not isinstance(current, TwinModel):
                raise TypeError()

            # start with the current state
            prediction = current.copy()

            # PREDICTION AREA

            # simple velocity example
            prediction.x_pos += prediction.x_vel
            prediction.y_pos += prediction.y_vel
            prediction.z_pos += prediction.z_vel

            # END OF PREDICTION AREA

            # append the new prediction to our list of future states
            futures.append(prediction)

            # exit condition
            if _n == 1:
                return futures
            else:
                return predict_step(_n-1, futures[-1], futures, _environment, _instruction)

        return predict_step(n, self, [], environment, instruction)
