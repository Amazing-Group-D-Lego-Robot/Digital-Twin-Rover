# CALLS METHODS FROM TWIN AND ROVER TO SEND INSTRUCTIONS / POLL SENSORS AND STATE
from time import strftime, gmtime

from scipy.interpolate import interpolate

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

        self.predicted_dumb_state.to_csv(
            "./res/prediction_dumps/prediction_dump (" + strftime("%d-%m-%Y_%H-%M-%S", gmtime()) + ").csv")

    def open_dumb_prediction(self, path):
        self.predicted_dumb_state = pd.read_csv(path)
        self.dumb_predictor_row = 0

    def visualise_adv_dataframe(self, agent_num) -> bool:
        if self.predicted_dumb_state is None:
            print("Load a prediction before running predict!")
            return False

        if self.advanced_predictor_row >= len(self.predicted_adv_state):
            return False

        self.twin_system[agent_num].twin.update_from_prediction(
            self.predicted_adv_state.iloc[self.advanced_predictor_row],
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
        def parse_input_data(input_data: str) -> list[dict]:
            """
            Parses input data to a dictionary as a list
            :param input_data: a string containing the instruction and 22 headers
            :return: A list of dictionaries that has a string instruction as a key and a value as a pandas dataframe
            """

            entries = input_data.split('\n')

            instructions = []
            instruction = []

            for entry in entries:
                if entry[:2] == "I:":
                    instructions.append(instruction)
                    instruction = []
                instruction.append(entry)

            instructions.append(instruction)
            instructions = instructions[1:]

            structured_data = []
            headers = ["time", "front_r", "front_g", "front_b", "front_intensity", "rear_r", "rear_g", "rear_b",
                       "rear_intensity", "distance_sensor", "accelerometer_x", "accelerometer_y", "accelerometer_z",
                       "yaw",
                       "pitch", "roll", "gyro_x", "gyro_y", "gyro_z", "steering_motor_position",
                       "driving_motor_position",
                       "force_sensor_newton"]

            for instruction in instructions:
                instruction_string = instruction[0]

                instruction_measurements = instruction[1:]
                number_of_measurements = len(instruction_measurements) // 22
                structured_measurements = pd.DataFrame(columns=headers)

                for i in range(number_of_measurements):
                    measurements = instruction_measurements[i * 22:(i + 1) * 22]
                    measurements = [[None if m == 'None' else int(m) for m in measurements]]
                    row = pd.DataFrame(measurements, columns=headers)
                    structured_measurements = pd.concat([structured_measurements, row])

                structured_datum = {
                    "instruction": instruction_string,
                    "measurements": structured_measurements,
                }
                structured_data.append(structured_datum)

            return structured_data

        def load_txt(ipath):
            with open(ipath) as f:
                data = parse_input_data(f.read())

            instrucntions = [row["instruction"] for row in data]
            print(instrucntions)
            data = [row for row in data if row["instruction"].split(" ")[0] == "I:MOTOR"]

            ret = data[0]["measurements"]

            for i in range(1, len(data)):
                ret = pd.concat([ret, data[i]["measurements"]])

            ret.drop(ret.columns.difference(["yaw", "steering_motor_position", "driving_motor_position"]), 1,
                    inplace=True)

            return ret.copy()

        """
        Function for loading offline file
        :return data: Returns CSV data for conversion
        """

        df = load_txt(path)

        for j in range(len(df["steering_motor_position"])):
            if df["steering_motor_position"].iloc[j] > 150:
                df["steering_motor_position"].iloc[j] -= 360

        current_offset = 0

        for j in range(len(df["driving_motor_position"])):
            df["driving_motor_position"].iloc[j] += current_offset

            if j > 2:
                if abs(df["driving_motor_position"].iloc[j] - df["driving_motor_position"].iloc[
                    j - 1]) > 50:
                    current_offset -= df["driving_motor_position"].iloc[j] - \
                                      df["driving_motor_position"].iloc[j - 1]
                    df["driving_motor_position"].iloc[j] -= df["driving_motor_position"].iloc[j] - \
                                                                      df["driving_motor_position"].iloc[j - 1]

        current_offset = 0

        for j in range(len(df["yaw"])):
            df["yaw"].iloc[j] += current_offset

            if df["yaw"].iloc[j] < 0:
                current_offset += 360
                df["yaw"].iloc[j] += 360

        df["steering_motor_position"] -= int(df["steering_motor_position"].iloc[0])
        df["driving_motor_position"] -= int(df["driving_motor_position"].iloc[0])
        df["yaw"] -= int(df["yaw"].iloc[0])

        f_steer = interpolate.interp1d(list(range(len(df["steering_motor_position"]))),
                                       df["steering_motor_position"])
        f_drive = interpolate.interp1d(list(range(len(df["driving_motor_position"]))),
                                       df["driving_motor_position"])
        f_yaw = interpolate.interp1d(list(range(len(df["yaw"]))), df["yaw"])

        df['A'] = df.loc[:, 'driving_motor_position']
        df['B'] = df.loc[:, 'driving_motor_position']
        df['Yaw'] = df.loc[:, 'yaw']

        df.drop(df.columns.difference(["A", "B", "Yaw"]), 1, inplace=True)

        self.current_data = df
        self.current_row_primary = 0

    def data_remaining(self):
        basic = self.current_row_primary < len(self.current_data)
        dumb = self.dumb_predictor_row < len(self.predicted_dumb_state)

        return basic or dumb
