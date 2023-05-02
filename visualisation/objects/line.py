from ursina import Mesh, Entity
from ursina.shaders import basic_lighting_shader
from ursina import color
from objects.sphere import Sphere


class Line:
    def __init__(self, a: Sphere, b: Sphere, colour: list):
        self.entity = Entity(
            model=Mesh(vertices=[a.entity.position, b.entity.position], mode='line', thickness=5),
            shader=basic_lighting_shader,
            position=[a.entity.position, b.entity.position],
            color=color.rgb(colour[0], colour[1], colour[2])
        )
