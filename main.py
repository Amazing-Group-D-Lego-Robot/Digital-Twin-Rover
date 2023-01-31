# ENTRY POINT FOR WHOLE SYSTEM
import os
import random
import sys
from time import sleep, time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from controller.controller import Controller


def main():
    controller = Controller()
    controller.load_data("res/motor data, lego version.csv")

    sleep(2)

    # run the controller until we reach the end of the dataset
    while controller.update():
        sleep(0.1)


if __name__ == "__main__":
    main()

    # hacky solution to ursinanetworking not cleaning up its threads
    os._exit(0)
    sys.exit(0)
