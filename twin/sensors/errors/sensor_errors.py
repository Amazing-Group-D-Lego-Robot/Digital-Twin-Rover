class RGBSensorValueError(Exception):
    """Raised when shape of RGB array is incorrect"""

    def __init__(self, name, shape):
        self.message = f"{name}: Colour Sensor RGB + intensity must be a list length 4. Current length is {shape}"
        super().__init__(self.message)


class DistanceValueError(Exception):
    """If it is not None or an integer this error is raised"""

    def __init__(self, name, value):
        self.message = f"{name}: value for Distance sensor must be NoneType or int, {value} is type {type(value)}"
        super().__init__(self.message)


class AccelerationValueError(Exception):
    """If acceleration np array isn't the correct shape"""

    def __init__(self, name, value):
        self.message = f"{name}: Acceleration sensor was provided with value of shape {value.shape} correct shape is (3,)"
        super().__init__(self.message)


class GyroValueError(Exception):
    """If acceleration np array isn't the correct shape"""

    def __init__(self, name, value):
        self.message = f"{name}: Gyro sensor was provided with value of shape {value.shape} correct shape is (3,)"
        super().__init__(self.message)
