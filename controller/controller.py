# CALLS METHODS FROM TWIN AND ROVER TO SEND INSTrUCTIONS / POLL SENSORS AND STATE

from rover.rover import RoverControl
from twin.twin import TwinSystem

class Controller:
    def __init__(self):
        print("created a new controller")
        rover = RoverControl()
        twin = TwinSystem()