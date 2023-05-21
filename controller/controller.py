# CALLS METHODS FROM TWIN AND ROVER TO SEND INSTRUCTIONS / POLL SENSORS AND STATE
from time import strftime, gmtime

from agent.agent import AgentControl
from twin.twin_system import TwinSystem
from visualisation.networking.server import TwinServer
import pandas as pd


class Controller:
    def __init__(self, agent_count=1, headless=False):
        # TODO: real-time communication (further work)
        # self.agent = AgentControl()
        self.twin_system = [TwinSystem() for _ in range(agent_count)]
        if not headless:
            self.server = TwinServer(agent_count)

        self.current_data = None

        self.predicted_dumb_state = None
        self.predicted_adv_state = None
        self.predicted_env = None

        self.current_row_primary = 0
        self.dumb_predictor_row = 0
        self.advanced_predictor_row = 0

        self.xs = []
        self.ys = []
        self.yaws = []
        self.steer = []
        self.drive = []

    def update(self, agent_num) -> bool:
        if self.current_data is None:
            print("Load a dataset before running update!")
            return False

        if self.current_row_primary >= len(self.current_data):
            # print("xs:", self.xs)
            # print("ys:", self.ys)
            # self.current_row_primary += 1
            return False

        # TODO: Add instructions to the dataset then feed them in here
        #   self.twin_system[0].change_instruction("instruction here")
        self.twin_system[agent_num].update(self.current_data.iloc[self.current_row_primary])
        self.current_row_primary += 1

        self.server.update(agent_num, self.twin_system[agent_num].twin, self.twin_system[agent_num].environment)

        self.xs.append(float(self.twin_system[agent_num].twin.pos[0]))
        self.ys.append(float(self.twin_system[agent_num].twin.pos[2]))

        return True

    def visualise_dumb_dataframe(self, agent_num) -> bool:
        if self.predicted_dumb_state is None:
            print("Load a prediction before running predict!")
            return False

        if self.dumb_predictor_row >= len(self.predicted_dumb_state):
            return False

        self.twin_system[agent_num].twin.update_from_prediction(self.predicted_dumb_state.iloc[self.dumb_predictor_row],
                                                                cols=self.predicted_dumb_state.columns.values.tolist())
        self.dumb_predictor_row += 10

        self.server.update(agent_num, self.twin_system[agent_num].twin, self.twin_system[agent_num].environment)

        self.xs.append(float(self.twin_system[agent_num].twin.pos[0]))
        self.ys.append(float(self.twin_system[agent_num].twin.pos[2]))
        self.yaws.append(float(self.twin_system[agent_num].twin.sensors["Yaw"].value))
        self.steer.append(float(self.twin_system[agent_num].twin.sensors["C"].value))
        self.drive.append(float(self.twin_system[agent_num].twin.sensors["A"].value))

        return True

    def load_dumb_prediction(self, instructions):
        self.predicted_env, self.predicted_dumb_state = self.twin_system[0].predict_next(instructions)
        self.dumb_predictor_row = 0

        self.predicted_dumb_state.to_csv("./res/prediction_dumps/prediction_dump (" + strftime("%d-%m-%Y_%H-%M-%S", gmtime()) + ").csv")

    def open_dumb_prediction(self, path):
        self.predicted_dumb_state = pd.read_csv(path)
        self.dumb_predictor_row = 0

    def visualise_adv_dataframe(self, agent_num) -> bool:
        if self.predicted_dumb_state is None:
            print("Load a prediction before running predict!")
            return False

        if self.advanced_predictor_row >= len(self.predicted_adv_state):
            return False

        self.twin_system[agent_num].twin.update_from_prediction(self.predicted_adv_state.iloc[self.advanced_predictor_row],
                                                                cols=self.predicted_dumb_state.columns.values.tolist())
        self.advanced_predictor_row += 10

        self.server.update(agent_num, self.twin_system[agent_num].twin, self.twin_system[agent_num].environment)

        self.xs.append(float(self.twin_system[agent_num].twin.pos[0]))
        self.ys.append(float(self.twin_system[agent_num].twin.pos[2]))
        self.yaws.append(float(self.twin_system[agent_num].twin.sensors["Yaw"].value))
        self.steer.append(float(self.twin_system[agent_num].twin.sensors["C"].value))
        self.drive.append(float(self.twin_system[agent_num].twin.sensors["A"].value))

        return True

    def open_adv_prediction(self, path):
        self.predicted_adv_state = pd.read_csv(path)
        self.advanced_predictor_row = 0

    def load_data(self, path):
        """
        Function for loading offline file
        :return data: Returns CSV data for conversion
        """

        df = pd.read_csv(path)
        df.fillna(method="ffill", inplace=True)
        df.fillna(method="backfill", inplace=True)

        self.current_data = df
        self.current_row_primary = 0

    def data_remaining(self):
        basic = self.current_row_primary < len(self.current_data)
        dumb = self.dumb_predictor_row < len(self.predicted_dumb_state)

        return basic or dumb