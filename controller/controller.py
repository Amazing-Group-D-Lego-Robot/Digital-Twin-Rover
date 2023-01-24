# CALLS METHODS FROM TWIN AND ROVER TO SEND INSTrUCTIONS / POLL SENSORS AND STATE

from rover.rover import RoverControl
from twin.twin import TwinSystem

class Controller:
    def __init__(self):
        print("made a new controller")
        rover = RoverControl
        twin = TwinSystem