import pandas as pd

from pytest import raises
from tkinter import filedialog as fd
from os import path


from twin.predictors.dumb_predictor import DumbPredictor
from twin.predictors.errors.predictor_exceptions import MotorPortError
from controller.test_input_data_parser import parse_input_data

dirname = path.dirname(__file__)[:-21]
filename = path.join(dirname, 'res/rover_readings/reading_three_instructions.txt')

with open(filename, 'r') as file:
    file_info = file.read()

print(file_info)



