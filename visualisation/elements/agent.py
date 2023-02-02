from ursina import Entity


class Agent(Entity):
    """
    Agent class where functions relating to the digital aspect of a twin are stored.
    """
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
