from copy import deepcopy


class TwinEnvironment:
    def __init__(self):
        print("created new environment")

    def copy(self):
        # copy function for making predictions
        return deepcopy(self)

    def update(self, sensor_data, instruction):
        # update state based upon truths
        pass
