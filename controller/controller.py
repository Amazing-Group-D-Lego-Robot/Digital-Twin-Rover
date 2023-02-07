# CALLS METHODS FROM TWIN AND ROVER TO SEND INSTrUCTIONS / POLL SENSORS AND STATE

from agent.agent import AgentControl
from twin.twin_system import TwinSystem
from visualisation.networking.server import TwinServer

import pandas as pd


class Controller:
    def __init__(self):
        self.agent = AgentControl()
        self.twin_system = TwinSystem()
        self.server = TwinServer()

        self.current_data = None
        self.current_row = 0

    def update(self) -> bool:
        if self.current_data is None:
            print("Load a dataset before running update!")
            return False

        if self.current_row >= len(self.current_data):
            return False

        # TODO: Add instructions to the dataset then feed them in here
        self.twin_system.update(self.current_data.iloc[self.current_row], instruction=None)
        self.current_row += 1

        self.server.update(self.twin_system.twin, self.twin_system.environment)

        return True

    def load_data(self, path):
        """
        Function for loading offline file
        :return data: Returns CSV data for conversion
        """

        df = pd.read_csv(path)
        df.fillna(method="ffill", inplace=True)
        df.fillna(method="backfill", inplace=True)

        self.current_data = df
        self.current_row = 0
