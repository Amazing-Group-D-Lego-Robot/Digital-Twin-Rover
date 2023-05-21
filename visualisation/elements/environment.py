from objects.block import Block
from objects.sphere import Sphere
from objects.line import Line
import json

from ursina import color


class SimulatedEnvironment:
    def __init__(self):
        # test_block = Block([5, 0, 5], [.25, .25, .25], color.pink)
        self.waypoint_lines = None
        self.waypoint_markers = None
        self.waypoints = None
        self.selected_block = 0
        self.selection_orb = Sphere([0, 0], color.pink)
        self.blocks = []
        self.border_nodes = []
        self.origin_offset = [0, 0]

        self.environment_filename = 'assets/environment.json'
        self.environment = self.load_environment()

        self.parse_environment_file()

    def load_environment(self):
        with open(self.environment_filename) as f:
            return json.load(f)

    def move_selection_orb(self):
        self.selected_block = self.selected_block % len(self.blocks)
        block_pos = self.blocks[self.selected_block].centre
        self.selection_orb.entity.position = [block_pos[0], self.blocks[self.selected_block].height, block_pos[1]]

    def parse_environment_file(self):
        # get origin (this can be merged with the main loop if there is an ordering where origin is always first
        for structure in self.environment:
            if structure['shape'] == 'origin':
                self.origin_offset = structure["centre"]
                # self.origin_offset = [0, 0]
                break

        # create blocks
        for structure in self.environment:
            if structure['shape'] != 'quad': continue

            # apply offset
            centre = structure["centre"].copy()
            # centre[0] -= self.origin_offset[0]
            # centre[1] -= self.origin_offset[1]

            points = structure["points"].copy()
            for point in points:
                # point[0] -= self.origin_offset[0]
                # point[1] -= self.origin_offset[1]
                Sphere(point, structure['colour'])

            self.blocks.append(Block(points, structure['height'], centre, structure['colour']))

        # create border
        for structure in self.environment:
            if structure['shape'] != 'border': continue

            curr_structure = []

            points = structure["points"].copy()
            for point in points:
                # point[0] -= self.origin_offset[0]
                # point[1] -= self.origin_offset[1]

                new_sphere = Sphere(point, structure['colour'])
                curr_structure.append(new_sphere)
                self.border_nodes.append(new_sphere)

            # Draw lines between points
            tmp_points = curr_structure.copy() + [curr_structure[0]]
            for i in range(len(tmp_points) - 1):
                Line(tmp_points[i], tmp_points[i + 1], structure['colour'])

        self.selected_block = 0
        self.move_selection_orb()

    def draw_waypoints(self, waypoints):
        # clear old waypoints
        if self.waypoint_markers is not None:
            for marker in self.waypoint_markers:
                marker.entity.enabled = False

        if self.waypoint_lines is not None:
            for line in self.waypoint_lines:
                line.entity.enabled = False

        self.waypoints = waypoints
        self.waypoint_markers = []
        self.waypoint_lines = []

        for waypoint in waypoints:
            self.waypoint_markers.append(Sphere(waypoint, color.blue, scale=5))

        # Draw lines between points
        tmp_points = self.waypoint_markers.copy()
        for i in range(len(tmp_points) - 1):
            self.waypoint_lines.append(Line(tmp_points[i], tmp_points[i + 1], color.blue))
