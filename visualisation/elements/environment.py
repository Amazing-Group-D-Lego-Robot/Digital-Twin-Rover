from objects.block import Block
from objects.sphere import Sphere
import json


class SimulatedEnvironment:
    def __init__(self):
        # test_block = Block([5, 0, 5], [.25, .25, .25], color.pink)
        self.blocks = []
        self.border_nodes = []
        self.origin_offset = [0, 0]


        self.environment_filename = 'assets/environment.json'
        self.environment = self.load_environment()

        self.parse_environment_file()

    def load_environment(self):
        with open(self.environment_filename) as f:
            return json.load(f)

    def parse_environment_file(self):
        # get origin (this can be merged with the main loop if there is an ordering where origin is always first
        for structure in self.environment:
            if structure['shape'] == 'origin':
                self.origin_offset = structure["centre"]
                break

        # create blocks
        for structure in self.environment:
            if structure['shape'] != 'quad': continue

            print(structure['points'], structure['height'], structure['colour'])

            # apply offset
            centre = structure["centre"].copy()
            centre[0] -= self.origin_offset[0]
            centre[1] -= self.origin_offset[1]

            points = structure["points"].copy()
            for point in points:
                point[0] -= self.origin_offset[0]
                point[1] -= self.origin_offset[1]

            self.blocks.append(Block(points, structure['height'], centre, structure['colour']))

        # create border
        for structure in self.environment:
            if structure['shape'] != 'border': continue

            points = structure["points"].copy()
            for point in points:
                point[0] -= self.origin_offset[0]
                point[1] -= self.origin_offset[1]

                self.border_nodes.append(Sphere(point, structure['colour']))
