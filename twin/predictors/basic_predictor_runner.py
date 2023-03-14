from  basic_predictor import basic_predictor
from controller.input_data_parser import parse_input_data

test = basic_predictor()
str = open('test.txt', 'r').read()
parsed_data = parse_input_data(str)
current_dict = parsed_data[0]
instruction = current_dict.get("instruction")
state = current_dict.get("measurements")

val = test.predict_instruction(instruction=instruction,current_state=state)
print(val)