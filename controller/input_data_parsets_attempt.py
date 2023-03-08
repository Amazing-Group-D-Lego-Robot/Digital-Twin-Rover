from input_data_parser import parse_input_data
import pandas as pd

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


val = parse_input_data(input_data)
print(len(val))
for point in list(val):
    print(f"{point.keys()}")
    print(point.get("instruction"))

    pd.options.display.max_colwidth = 25
    # with pd.option_context('display.max_seq_items', None):
    print(point.get("measurements").head())
    break
