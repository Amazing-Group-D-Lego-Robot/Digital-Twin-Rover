# ENTRY POINT FOR WHOLE SYSTEM
import os
import random
import sys
from time import sleep

import numpy as np

from controller.controller import Controller


def main():
    controller = Controller()


if __name__ == "__main__":
    main()

    # hacky solution to ursinanetworking not cleaning up its threads
    os._exit(0)
    sys.exit(0)
