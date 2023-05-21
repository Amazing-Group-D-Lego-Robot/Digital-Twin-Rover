from ursina import Mesh, Entity
from ursina.shaders import basic_lighting_shader
from ursina import color


class Block:
    def __init__(self, coords: list, height: int, centre: list, colour: list):

        self.height = height
        self.centre = centre

        mesh = Mesh(vertices=[
            [coords[1][0], 0, coords[1][1]],        # 0
            [coords[2][0], 0, coords[2][1]],        # 1
            [coords[2][0], height, coords[2][1]],   # 2
            [coords[1][0], height, coords[1][1]],   # 3
            [coords[0][0], 0, coords[0][1]],        # 4
            [coords[3][0], 0, coords[3][1]],        # 5
            [coords[3][0], height, coords[3][1]],   # 6
            [coords[0][0], height, coords[0][1]],   # 7
            ],

            triangles=[
                [3, 2, 1, 0],
                [0, 1, 5, 4],
                [1, 2, 6, 5],
                [2, 3, 7, 6],
                [3, 0, 4, 7],
                [4, 5, 6, 7],
            ],
            normals=[
                [-1, -1, -1],   # 0
                [1, -1, -1],    # 1
                [1, -1, 1],     # 2
                [-1, -1, 1],    # 3
                [-1, 1, -1],    # 4
                [1, 1, -1],     # 5
                [1, 1, 1],      # 6
                [-1, 1, 1],     # 7
            ])

        self.entity = Entity(
            model=mesh,
            shader=basic_lighting_shader,
            # position=[centre[0], 0, centre[1]],
            color=color.rgb(colour[0], colour[1], colour[2]))
