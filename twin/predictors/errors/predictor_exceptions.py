class MotorPortError(Exception):
    """Raised when the port referenced for instruction MOTOR is invalid"""
    def __init__(self, port):
        self.message = f"Port {port} is not a valid motor port"
        super().__init__(self.message)
