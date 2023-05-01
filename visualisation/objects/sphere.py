from ursina import Mesh, Entity
from ursina.shaders import basic_lighting_shader
from ursina import color


class Sphere:
    def __init__(self, centre: list, colour: list, scale=0.5):
        self.entity = Entity(
            model='sphere',
            shader=basic_lighting_shader,
            position=[centre[0], 0, centre[1]],
            color=color.rgb(colour[0], colour[1], colour[2]),
            scale=scale,
        )
