from objects.block import Block
from objects.slope import Slope
import json


class SimulatedEnvironment:
    def __init__(self):
        # test_block = Block([5, 0, 5], [.25, .25, .25], color.pink)
        self.blocks = []
        self.slopes = []

        self.environment_filename = 'assets/environment.json'
        self.environment = self.load_environment()

        self.parse_environment_file()

    def load_environment(self):
        with open(self.environment_filename) as f:
            return json.load(f)

    def parse_environment_file(self):
        for structure in self.environment:
            if structure['shape'] == 'origin': continue

            print(structure['points'], structure['height'], structure['colour'])

            self.blocks.append(Block(structure['points'], structure['height'], structure['centre'], structure['colour']))
