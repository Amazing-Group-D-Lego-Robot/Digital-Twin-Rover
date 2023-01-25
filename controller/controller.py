# CALLS METHODS FROM TWIN AND ROVER TO SEND INSTrUCTIONS / POLL SENSORS AND STATE

from rover.rover import RoverControl
from twin.twin import TwinSystem

class Controller:
    def __init__(self):
        print("created a new controller")
        self.rover = RoverControl()
        self.twin = TwinSystem()
    
    def send_to_rover(self):
        """
        Passes information to rover
        """
        pass

    def send_to_twin(self):
        """
        Passes info to twin
        """
        pass

    def receive_from_twin(self):
        """
        Function to digest twin input
        """

        pass
    
    def receive_from_rover(self):
        """
        Function to digest rover input
        """
        pass