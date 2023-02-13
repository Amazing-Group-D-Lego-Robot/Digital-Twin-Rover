from objects.block import Block
from objects.slope import Slope
from ursina import color


class SimulatedEnvironment:
    def __init__(self):
        # test_block = Block([5, 0, 5], [.25, .25, .25], color.pink)
        self.blocks = []
        self.slopes = []

        self.generate_test_blocks()
        self.generate_test_slopes()

    def generate_test_blocks(self):
        possible_colours = [color.white, color.smoke, color.black, color.red, color.yellow,
                            color.lime, color.blue, color.pink, color.brown, color.gold]
        for i in range(10):
            self.blocks.append(Block([4*i, 0, 1], [.25*i, .25*i, .25*i], possible_colours[i]))

    def generate_test_slopes(self):
        possible_colours = [color.white, color.smoke, color.black, color.red, color.yellow,
                            color.lime, color.blue, color.pink, color.brown, color.gold]
        for i in range(10):
            self.slopes.append(Slope([4 * i, 0, 4], [.25 * i, .25 * i, .25 * i], possible_colours[i]))

