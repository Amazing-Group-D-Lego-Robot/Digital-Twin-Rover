from ursina import Entity, Vec3
from elements.sensor_ray import SensorRay


class Agent(Entity):
    """
    Agent class where functions relating to the digital aspect of a twin are stored.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sensor_rays = []

    def add_sensor(self, offset: Vec3, direction: Vec3 = Vec3(0, 0, 1)):
        self.sensor_rays.append(SensorRay(self, offset, direction))

    def move_to(self, pos: list):
        """
        Move the agent to a particular [x, y, z] position
        :param pos:
        :return:
        """
        self.animate_position(pos, duration=0.1)

    def rotate_to(self, rot: list):
        """
        Rotate the agent to point towards a particular [x, y, z] position
        :param rot:
        :return:
        """
        self.animate_rotation(rot, duration=0.1)
