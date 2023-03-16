import pandas as pd

from twin.twin_designs.dumb_twin import DumbPredictor
from controller.test_input_data_parser import parse_input_data
from twin.twin_designs.errors.twin_exceptions import MotorPortError
from pytest import raises

input_data = """I:MOTOR C 25 720
5
2
1
2
4
0
2
0
1
None
-27
67
-997
34
3
178
0
0
0
85
207
0
I:MOTOR A 25 -10
6
1
1
0
3
0
0
0
1
None
-28
70
-997
34
3
178
0
0
0
85
220
0
140
1
1
0
4
0
2
0
1
None
-27
69
-996
34
3
178
0
0
0
85
220
0
I:WAIT 1"""

data = parse_input_data(input_data)
dumb_predictor = DumbPredictor()


def test_WAIT_reading_start():
    """checks wait on new initialisation of prediction function with 0 for rows is returned"""
    predictor = DumbPredictor()

    with raises(TypeError):
        df = predictor.predict_instruction(data[2].get("instruction"), data[2].get("measurements"))


def test_WAIT_after_previous():
    """Test wait for when ran after a previous functions"""
    expected = data[1].get("measurements")

    dumb_predictor.predict_instruction(data[1].get("instruction"), expected)
    actual = dumb_predictor.predict_instruction("I:WAIT", data[2].get("measurements"))

    assert actual.equals(expected)


def test_BEEP_reading():
    expected = data[0].get("measurements")  # use random dataframe since it should just return this
    df = dumb_predictor.predict_instruction("I:BEEP", expected)

    assert df.equals(expected)


def test_MOTOR_PORT_error():
    with raises(MotorPortError):
        dumb_predictor.predict_instruction("I:MOTOR Z 100", pd.DataFrame())


def test_Driving_Motor_forward():
    curr_data = data[0]

    inst = curr_data.get("instruction")
    state = curr_data.get("measurements")

    results = dumb_predictor.predict_instruction(inst, state)

    val = int(results["driving_motor_position"][-1:])
    assert val == 207 and results.shape == (721, 22)


def test_Driving_Motor_Backward():

    curr_data = data[0]

    inst = curr_data.get("instruction")
    state = curr_data.get("measurements")

    results = dumb_predictor.predict_instruction("I:MOTOR C 25 -720", state)

    val = int(results["driving_motor_position"][-1:])
    assert val == 207 and results.shape == (721, 22)


def test_Steering_Motor_right():
    state = data[0].get("measurements")
    results = dumb_predictor.predict_instruction(f"I:MOTOR A 25 10", state)

    val = int(results["steering_motor_position"][-1:])
    assert val == 95 and results.shape == (11, 22)


def test_Steering_Motor_left():
    state = data[0].get("measurements")
    results = dumb_predictor.predict_instruction("I:MOTOR A 25 -10", state)

    val = int(results["steering_motor_position"][-1:])
    assert val == 75 and results.shape == (11, 22)
