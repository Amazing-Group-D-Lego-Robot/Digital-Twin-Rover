# CALLS METHODS FROM TWIN AND ROVER TO SEND INSTrUCTIONS / POLL SENSORS AND STATE

from agent.agent import AgentControl
from twin.twin import TwinSystem
from visualisation.networking.server import TwinServer
from menu.main_menu import MainMenu
import pandas as pd


class Controller:
    def __init__(self):
        #print("created a new controller")

        self.agent = AgentControl()
        self.twin = TwinSystem()
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
        self.twin.update(self.current_data.iloc[self.current_row], instruction=None)
        self.current_row += 1

        self.server.update(self.twin.worldstate)

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

    # def send_to_agent(self):
    #     """
    #     Passes information to agent
    #     """
    #     pass

    # def send_to_twin(self) -> pd.DataFrame:
    #     """
    #     Passes info to twin
    #     :return current_data: pandas dataframe of the current available
    #     """
    #     # TODO: Make this send to the controller rather than return the data TODO: Talk to Will and Callum about what
    #     #  they want doing here (This is a work in progress as I assume the controller predicts
    #     return self.current_data

    # def receive_from_twin(self):
    #     """
    #     Function to digest twin input
    #     """
    #
    #     pass

    # def receive_from_agent(self, is_online:bool = False):
    #     """
    #     Function to digest agent input
    #     :param is_online: boolean value to indicate if the agent is live or not
    #     # """
    #     # if is_online:
    #     #     return -1
    #     #
    #     # self.current_data = self.offline_load_csv()
