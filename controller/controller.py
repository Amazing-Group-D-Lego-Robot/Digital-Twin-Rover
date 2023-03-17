# CALLS METHODS FROM TWIN AND ROVER TO SEND INSTRUCTIONS / POLL SENSORS AND STATE
from time import strftime, gmtime

from agent.agent import AgentControl
from twin.twin_system import TwinSystem
from visualisation.networking.server import TwinServer
import pandas as pd


class Controller:
    def __init__(self, headless=False):
        # TODO: real-time communication (further work)
        # self.agent = AgentControl()
        self.twin_system = TwinSystem()
        if not headless:
            self.server = TwinServer()

        self.current_data = None

        self.predicted_state = None
        self.predicted_env = None

        self.current_row = 0

    def update(self) -> bool:
        if self.current_data is None:
            print("Load a dataset before running update!")
            return False

        if self.current_row >= len(self.current_data):
            return False

        # TODO: Add instructions to the dataset then feed them in here
        #   self.twin_system.change_instruction("instruction here")
        self.twin_system.update(self.current_data.iloc[self.current_row])
        self.current_row += 1

        self.server.update(self.twin_system.twin, self.twin_system.environment)

        return True

    def visualise_dataframe(self) -> bool:
        if self.predicted_state is None:
            print("Load a prediction before running predict!")
            return False

        if self.current_row >= len(self.predicted_state):
            return False

        self.twin_system.twin.update_from_prediction(self.predicted_state.iloc[self.current_row],
                                                     cols=self.predicted_state.columns.values.tolist())
        self.current_row += 1

        self.server.update(self.twin_system.twin, self.twin_system.environment)

        return True

    def load_prediction(self, instructions):
        self.predicted_env, self.predicted_state = self.twin_system.predict_next(instructions)
        self.current_row = 0

        self.predicted_state.to_csv("./res/prediction_dumps/prediction_dump (" + strftime("%d-%m-%Y_%H-%M-%S", gmtime()) + ").csv")

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
