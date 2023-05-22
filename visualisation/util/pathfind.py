from subprocess import run
from util.rrt.main import rrt_start
from util.generate import SF
import os
import cv2
from objects.sphere import Sphere


def predict_path(agent_pos, target_block, target_block_pos):
    # Select the correct image
    cwd = os.getcwd()
    image_directory = os.path.join(cwd, "../res/environments/")
    target_image = os.path.join(image_directory, f"map-{target_block}.png")
    if not os.path.exists(target_image):
        raise FileNotFoundError(f"Image not found: {target_image}")

    print(f"Target image: {target_image}")
    image_obj = cv2.imread(target_image)
    image_height = image_obj.shape[0]
    image_width = image_obj.shape[1]

    # get the start and goal position
    # start_pos = (round(agent_pos[2]/SF), round(agent_pos[0]/SF))
    start_pos = (round(agent_pos[0] / SF), round(image_height - agent_pos[2] / SF))

    target_block_pos = (round(target_block_pos[0]/SF), round(target_block_pos[1]/SF))
    print(f"Predicting path from {agent_pos} to {target_block_pos}")

    # pass this to rrt algorithm
    found_path = rrt_start(start_pos, tuple(target_block_pos), target_image)
    corrected_path = [(node[1], image_height-node[0]) for node in found_path]

    # get the path
    print("Path found!" + corrected_path.__str__())
    return corrected_path
