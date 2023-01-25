from twin.twin_model import TwinModel
from twin.twin_environment import TwinEnvironment


class WorldState:
    def __init__(self):
        # print("created new world state")

        self.twin = TwinModel()
        self.environment = TwinEnvironment()
