import pandas as pd

from pytest import raises
from tkinter import filedialog as fd
from os import path


from twin.predictors.dumb_predictor import DumbPredictor
from twin.predictors.errors.predictor_exceptions import MotorPortError
from controller.test_input_data_parser import parse_input_data

file_read = None
print(path.dirname(__file__))



