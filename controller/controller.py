# CALLS METHODS FROM TWIN AND ROVER TO SEND INSTrUCTIONS / POLL SENSORS AND STATE

from rover.rover import RoverControl
from twin.twin import TwinSystem

import sys
import pandas as pd


class Controller:
    def __init__(self):
        print("created a new controller")
        self.rover = RoverControl()
        self.twin = TwinSystem()
        self.current_data = None
        self.offline_file_location = "/home/charlie/Documents/Hardware/FirstModel/motor data, human version.csv"

    def send_to_rover(self):
        """
        Passes information to rover
        """
        pass

    def send_to_twin(self) -> pd.DataFrame:
        """
        Passes info to twin
        :return current_data: pandas dataframe of the current available
        """
        return self.current_data


    def receive_from_twin(self):
        """
        Function to digest twin input
        """

        pass

    def receive_from_rover(self, is_online:bool = False):
        """
        Function to digest rover input
        :param is_online: boolean value to indicate if the rover is live or not
        """
        if is_online:
            return -1

        self.current_data = self.offline_load_csv()

    def offline_load_csv(self) -> pd.DataFrame:
        """
        Function for loading offline file
        :param location: current location of offline file
        :return data: Returns CSV data for conversion
        """

        df = pd.read_csv(self.offline_file_location)
        df.fillna(method="ffill", inplace=True)
        df.fillna(method="backfill", inplace=True)
        return df
