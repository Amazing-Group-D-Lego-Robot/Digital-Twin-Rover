from ursina import Mesh, Entity
from ursina.shaders import basic_lighting_shader
from ursina import color


class Sphere:
    def __init__(self, centre: list, colour: list):
        entity = Entity(
            model='sphere',
            shader=basic_lighting_shader,
            position=[centre[0], 0, centre[1]],
            color=color.black,
            scale=0.1,
        )
