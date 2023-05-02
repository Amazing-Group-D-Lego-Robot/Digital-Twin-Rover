from util.rrt.config import *
from util.rrt.rrt import rrt
import util.rrt.drawing
import pygame as pg

pg.init()


def rrt_start(start_pos, goal_pos, image_path):
    util.rrt.drawing.loadObstacles(image_path)

    util.rrt.drawing.startPos = start_pos
    util.rrt.drawing.goalPos = goal_pos
    tree = rrt(util.rrt.drawing.startPos, util.rrt.drawing.goalPos, util.rrt.drawing.obstaclesSurface)

    # A path was found
    util.rrt.drawing.clearEdgesPool()
    path = util.rrt.drawing.get_path(tree, image_path)

    # minus each y value from the height of the image
    corrected_path = [(node[1], node[0]) for node in path]

    pg.quit()

    return corrected_path
