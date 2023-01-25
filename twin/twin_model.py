from copy import deepcopy
from time import time_ns


class TwinModel:
    def __init__(self):
        # print("created new twin")

        # META INFO
        self.last_update_time = -1

        # POSITIONAL INFO
        self.x_pos = 0  # relative x-axis displacement from start position
        self.y_pos = 0  # relative y-axis displacement from start position
        self.z_pos = 0  # relative z-axis displacement from start position

        self.x_vel = 0  # x-axis velocity from start position
        self.y_vel = 0  # y-axis velocity from start position
        self.z_vel = 0  # z-axis velocity from start position

        self.x_acc = 0  # x-axis acceleration from start position (read directly from sensors)
        self.y_acc = 0  # y-axis acceleration from start position (read directly from sensors)
        self.z_acc = 0  # z-axis acceleration from start position (read directly from sensors)

        self.x_rot = 0  # x-axis rotation from upright (read directly from sensors)
        self.y_rot = 0  # y-axis rotation from upright (read directly from sensors)
        self.z_rot = 0  # z-axis rotation from upright (read directly from sensors)

        # SENSORS
        self.distance_sensor = 0  # number of mm to the nearest object ahead of the sensor
        self.motor0_rot = 0  # rotation in degrees of motor 0
        self.motor1_rot = 0  # rotation in degrees of motor 1
        self.motor2_rot = 0  # rotation in degrees of motor 2
        self.motor3_rot = 0  # rotation in degrees of motor 3

    def copy(self):
        # copy function for making predictions
        return deepcopy(self)

    def update(self, sensor_data, instruction, environment):
        # update state based upon truths and environment

        if sensor_data is not None:
            # TODO: Update sensors when we have a structure for them
            pass

        if instruction is not None:
            # TODO: Update state with instruction when we have a structure for them
            pass

        # UPDATE POSITION
        # if we are not on our first update
        if self.last_update_time != -1:
            # time difference since last update in seconds
            time_delta = (time_ns() - self.last_update_time) / 1_000_000_000
            if time_delta == 0:
                time_delta = 0.000000001

            # acceleration and rotation already updated with sensor update

            self.x_vel += self.x_acc * time_delta
            self.y_vel += self.y_acc * time_delta
            self.z_vel += self.z_acc * time_delta

            self.x_pos += self.x_vel * time_delta
            self.y_pos += self.y_vel * time_delta
            self.z_pos += self.z_vel * time_delta

        # reset clock
        self.last_update_time = time_ns()

    def predict_next(self, n=1, environment=None, instruction=None):
        # predict based upon a possible new instruction and simulated sensor data gathered
        # from the environment

        def predict_step(_n, current, futures, _environment, _instruction):
            if not isinstance(current, TwinModel):
                raise TypeError()

            # start with the current state
            prediction = current.copy()

            # PREDICTION AREA

            # simple movement example
            self.x_vel += self.x_acc
            self.y_vel += self.y_acc
            self.z_vel += self.z_acc

            self.x_pos += self.x_vel
            self.y_pos += self.y_vel
            self.z_pos += self.z_vel

            # END OF PREDICTION AREA

            # append the new prediction to our list of future states
            futures.append(prediction)

            # exit condition
            if _n == 1:
                return futures
            else:
                return predict_step(_n-1, futures[-1], futures, _environment, _instruction)

        return predict_step(n, self, [], environment, instruction)
