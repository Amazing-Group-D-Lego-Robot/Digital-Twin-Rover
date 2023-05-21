"""
This is the module responsible for handling drawings to the screen.
All pygame.draw commands must be executed inside this module.
It also contains important variables related to drawing and other uses,
  that are accessible by other modules, such as startPos and goalPos. 
"""
from util.rrt.config import *
import cv2

# Initialize start and goal positions:
startPos = START_INIT_POS
goalPos = GOAL_INIT_POS

# Surfaces drawn to the screen:
obstaclesSurface = None

# Edges pool to avoid updating the screen every time a new edge is added:
edgesPool = []

# Show or not the information about the algorithm:
showInfo = False


def addEdge(edge):
    global edgesPool
    edgesPool.append(edge)
    if len(edgesPool) >= MAX_EDGES_POOL:
        edgesPool = []


def clearEdgesPool():
    global edgesPool
    edgesPool = []


def loadObstacles(image_path):
    global obstaclesSurface
    obstaclesSurface = cv2.imread(image_path)
    WIDTH = obstaclesSurface.shape[0]
    HEIGHT = obstaclesSurface.shape[1]
    print(f"Loading image of dimensions {obstaclesSurface.shape} from file {image_path}")


def get_path(parent, output_path):
    curr_path = []
    current = goalPos
    # Follow the parent nodes until the start position is reached:
    while parent[goalPos] and current is not None:
        cv2.circle(obstaclesSurface, current, 5, (0, 0, 255), -1)
        curr_path.append(current)
        current = parent[current]

    # Draw the path:
    for i in range(len(curr_path) - 1):
        cv2.line(obstaclesSurface, curr_path[i], curr_path[i + 1], (0, 255, 0), 2)

    cv2.imwrite(output_path.replace(".png", '-output.png'), obstaclesSurface)
    return curr_path
