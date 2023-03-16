class RGBValueError(Exception):
    """Raised when shape of RGB array is incorrect"""

    def __init__(self, name, shape, typ):
        self.message = f"{name}: RGB + intensity must be a list length 4\n Current length is {shape} with type {typ}"
        super().__init__(self.message)


class AccelerationValueError(Exception):
    """If list is not correct length or type raise this error"""

    def __init__(self, name, shape, typ):
        self.message = f"{name}: XYZ value must be a list list of length 4\n Current length is {shape} with type {typ}"
        super().__init__(self.message)


class DistanceValueError(Exception):
    """If it is not None or an integer this error is raised"""

    def __init__(self, name, value):
        self.message = f"{name}: value for sensor must be NoneType or int, {value} is type {type(value)}"
        super().__init__(self.message)

class GeneralSensorValueError(Exception):
    """If a general sensor isn't fed updated value of type int"""

    def __init__(self,name,value):
        self.message = f"{name}: sensor must receive int. Value: {value} is of type {type(value)}"