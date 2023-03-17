import json
from copy import deepcopy


class Box:
    def __init__(self, points, colour):
        # anti-clockwise ordering
        self.points = points
        # r g b
        self.colour = colour


class TwinEnvironment:
    def __init__(self):
        # TODO: dynamic environment (future work)
        # self.observed_points = []  # All points that the agent has "seen" with sensors
        self.world = []  # All pre-programmed objects

        self.environment_filename = 'res/environment.json'
        self.environment = self.load_environment()

        self.parse_environment_file()

    def load_environment(self):
        with open(self.environment_filename) as f:
            return json.load(f)

    def parse_environment_file(self):
        for structure in self.environment:
            if structure['shape'] == 'origin': continue

            print(structure['points'], structure['height'], structure['colour'])

            self.world.append(Box(structure['points'], structure['colour']))

    def copy(self):
        # copy function for making predictions
        return deepcopy(self)
