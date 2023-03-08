import pandas as pd
from .input_data_parser import parse_input_data

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


def test_parse_input_data_type():
    """Checks input parser is a list"""
    out = parse_input_data(input_data)
    assert type(out) == list


def test_parse_input_inner_data_type():
    """Check all data types are of type dictionary"""
    assert all(isinstance(x, dict) for x in parse_input_data(input_data))


def test_parse_input_measurement_dataframe():
    """Checks all measurements are a dataframe"""
    assert all(isinstance(x.get("measurements"), pd.DataFrame) for x in parse_input_data(input_data))


def test_parse_input_values():
    """Tests that the order of values in the dataframes are what is expected by the original data"""
    val = parse_input_data(input_data)
    data = input_data.split("\n")
    values = []

    # get unparsed values in correct order
    for point in data:
        if point[0] == 'I':
            continue
        elif point == "None":
            values.append(None)
        else:
            values.append(int(point))

    # get values from dataframes in order
    found_measure = []
    for dic in val:
        measure = dic.get("measurements")
        for m in measure.values:
            for v in m:
                found_measure.append(v)

    # compare parsed and unparsed values
    assert all([x == y for (x, y) in zip(found_measure, values)])
