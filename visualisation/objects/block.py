from ursina import Mesh, Entity
from ursina.shaders import basic_lighting_shader


class Block:
    def __init__(self, pos: list, scale: list, colour: str):
        p_x, p_y, p_z = pos
        s_x, s_y, s_z = scale

        mesh = Mesh(vertices=[
            [0*s_x, 0*s_y, 0*s_z],  # 0
            [1*s_x, 0*s_y, 0*s_z],  # 1
            [1*s_x, 0*s_y, 1*s_z],  # 2
            [0*s_x, 0*s_y, 1*s_z],  # 3
            [0*s_x, 1*s_y, 0*s_z],  # 4
            [1*s_x, 1*s_y, 0*s_z],  # 5
            [1*s_x, 1*s_y, 1*s_z],  # 6
            [0*s_x, 1*s_y, 1*s_z],  # 7
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

        entity = Entity(
            model=mesh,
            shader=basic_lighting_shader,
            origin=pos,
            color=colour)
