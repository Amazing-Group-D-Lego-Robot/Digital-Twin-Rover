# ENTRY POINT FOR WHOLE SYSTEM
import random
from time import sleep

from controller.controller import Controller


def main():
    controller = Controller()

    # Proof of concept connection to show the twin server can send data

    controller.twin.worldstate.twin.x_acc = 0.1
    controller.twin.worldstate.twin.y_acc = 0.2
    controller.twin.worldstate.twin.z_acc = 0.3

    i = 0

    while True:
        if i % 100 == 0:
            controller.twin.worldstate.twin.x_acc = -0.5 + random.random()
            controller.twin.worldstate.twin.y_acc = -0.5 + random.random()
            controller.twin.worldstate.twin.z_acc = -0.5 + random.random()
            print("direction change")
            i = 0

        i += 1

        controller.twin.update()
        sleep(0.1)


if __name__ == "__main__":
    main()
