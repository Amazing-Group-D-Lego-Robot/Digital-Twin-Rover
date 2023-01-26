# ENTRY POINT FOR WHOLE SYSTEM
import os
import random
import sys
from time import sleep

from controller.controller import Controller


def main():
    controller = Controller()

    # Proof of concept connection to show the twin server can send data

    # controller.twin.worldstate.twin.x_acc = 0.1
    # controller.twin.worldstate.twin.y_acc = 0.2
    # controller.twin.worldstate.twin.z_acc = 0.3
    #
    # i = 0
    #
    # while i < 300:
    #     if i % 100 == 0:
    #         controller.twin.worldstate.twin.x_acc = -0.5 + random.random()
    #         controller.twin.worldstate.twin.y_acc = -0.5 + random.random()
    #         controller.twin.worldstate.twin.z_acc = -0.5 + random.random()
    #         print("direction change")
    #         #i = 0
    #
    #     i += 1
    #
    #     controller.twin.update()
    #     sleep(0.1)


if __name__ == "__main__":
    main()

    # hacky solution to ursinanetworking not cleaning up its threads
    os._exit(0)
    sys.exit(0)
