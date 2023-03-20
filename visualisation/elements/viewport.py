from ursina.prefabs.first_person_controller import FirstPersonController


class Viewport(FirstPersonController):
    """
    Class to abstract the FirstPersonController Ursina class, this allows a floating camera
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = 1

    def input(self, key):
        """
        FirstPersonController input function override
        :param key:
        :return:
        """
        if key == 'space':
            self.position += (0, 0.03, 0)

        if key == 'shift':
            self.position -= (0, 0.03, 0)

        if key == '1':
            self.speed = 1

        if key == '2':
            self.speed = 10

        if key == '3':
            self.speed = 100

        if key == 'u':
            self.position += (0, 0.3, 0)

        if key == 'j':
            self.position -= (0, 0.3, 0)

        if key == 'i':
            self.position += (0, 1, 0)

        if key == 'k':
            self.position -= (0, 1, 0)