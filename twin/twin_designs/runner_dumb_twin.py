from dumb_twin import DumbPredictor
from controller.test_input_data_parser import parse_input_data

input_data = input_data = """I:MOTOR C 25 720
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


def main(input_data):
    parsed = parse_input_data(input_data)
    predictor = DumbPredictor()

    print(parsed)

    for data in parsed:
        inst = data.get("instruction")
        state = data.get("measurements")
        result = predictor.predict_instruction(inst, state)
        print(result)


if __name__ == "__main__":
    main(input_data)
