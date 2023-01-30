# ENTRY POINT FOR WHOLE SYSTEM
import os
import random
import sys
from time import sleep

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from controller.controller import Controller


def main():
    controller = Controller()

    df = pd.read_csv("res/motor data, lego version.csv")
    df.fillna(method="ffill", inplace=True)
    df.fillna(method="backfill", inplace=True)

    sleep(10)

    for i in range(1, len(df)):
        controller.twin.update(sensor_info=df.iloc[i][["A", "B", "C", "Yaw"]])
        sleep(0.1)
        print(df.iloc[i]["timestamp"]/1000., controller.twin.worldstate.twin.pos)


if __name__ == "__main__":
    main()

    # hacky solution to ursinanetworking not cleaning up its threads
    os._exit(0)
    sys.exit(0)
