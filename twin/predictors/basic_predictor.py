import pandas as pd

from predictor import Predictor


class basic_predictor(Predictor):
    def __init__(self):
        super().__init__()

        self.wheel_diameter = 0.088  # diameter of the driving wheels in m
        self.movement_per_degree = (self.wheel_diameter * 3.141592654) / 360  # m of movement with 1 degree of turn

    def handle_motor(self, motor: str, speed: int, angle: int, current_state: pd.DataFrame) -> pd.DataFrame:
        # figure out if we are dealing with the drive motor or steering motor
        if motor == "C":  # steering
            # only one row needed as steering is "instant-ish"
            ret = current_state.copy(deep=True)
            ret["steering_motor_position"] += angle
            return ret

        if motor == "A":  # drive
            ret = current_state.copy(deep=True)
            # move the rover by one degree each row
            for i in range(angle):
                # TODO: use the value of "yaw", "steering_motor_position", etc to turn the rover when it moves forwards
                temp = ret.iloc[-1:].copy()
                temp["z_pos"] += self.movement_per_degree
                temp["driving_motor_position"] += 1
                ret = pd.concat([ret, temp])

            return ret

        # fallback if we don't know how to handle the specified motor
        return current_state.copy(deep=True)

    def handle_beep(self, time: int, current_state: pd.DataFrame) -> pd.DataFrame:
        # beeps don't actually do anything important
        return current_state.copy(deep=True)

    def predict_instruction(self, instruction: str, current_state: pd.DataFrame) -> pd.DataFrame:
        split_instruction = instruction.split(" ")
        print("opcode:", split_instruction[0])
        print("operands:", split_instruction[1:])

        # for I:MOTOR instructions
        if split_instruction[0] == "I:MOTOR":
            return self.handle_motor(motor=split_instruction[1], speed=int(split_instruction[2]),
                                     angle=int(split_instruction[3]), current_state=current_state)

        # for I:BEEP instructions
        if split_instruction[0] == "I:BEEP":
            return self.handle_beep(time=int(split_instruction[1]), current_state=current_state)

        # default fallback if we don't know how to handle the instruction
        return current_state.copy(deep=True)
