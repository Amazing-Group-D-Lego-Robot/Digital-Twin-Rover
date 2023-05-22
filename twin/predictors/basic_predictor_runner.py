from basic_predictor import BasicPredictor
from controller.input_data_parser import parse_input_data
from twin.twin_environment import TwinEnvironment

test = BasicPredictor()
str = open('../../res/rover_readings/reading_three_instructions.txt', 'r').read()
parsed_data = parse_input_data(str)
current_dict = parsed_data[0]
instruction = current_dict.get("instruction")
state = current_dict.get("measurements")
env = TwinEnvironment()

val = test.predict_instruction(env, instruction=instruction, current_state=state)
print(val)
