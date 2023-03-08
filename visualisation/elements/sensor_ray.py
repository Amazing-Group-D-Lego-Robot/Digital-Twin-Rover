from ursina import Entity, Mesh, Vec3


class SensorRay(Entity):
    """
    Class for handling sensors and linking them to the entity
    """
    def __init__(self, parent: Entity, offset: Vec3, direction=Vec3(0, 0, 1), **kwargs):
        super().__init__(model=Mesh(vertices=[parent.position + offset, parent.position + offset + direction], mode='line', thickness=4), **kwargs)
        #self.origin_x = parent.origin_x
        #self.origin_y = parent.origin_y
        #self.origin_z = parent.origin_z
        self.parent = parent

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
