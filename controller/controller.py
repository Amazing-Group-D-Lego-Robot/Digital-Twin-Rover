# CALLS METHODS FROM TWIN AND ROVER TO SEND INSTrUCTIONS / POLL SENSORS AND STATE

from rover.rover import RoverControl
from twin.twin import TwinSystem

import pandas as pd


class Controller:
    def __init__(self):
        print("created a new controller")
        self.rover = RoverControl()
        self.twin = TwinSystem()
        self.current_data = None

    def send_to_rover(self):
        """
        Passes information to rover
        """
        pass

    def send_to_twin(self):
        """
        Passes info to twin
        """
        pass

    def receive_from_twin(self):
        """
        Function to digest twin input
        """

        pass

    def receive_from_rover(self):
        """
        Function to digest rover input
        """
        pass


    def offline_load_file(self, location) :
        """
        Function for loading offline file
        :param location: current location of offline file
        :return status: Returns status code based on load
        :return data: Returns CSV data for conversion
        """
        pass

    def csv_to_dataframe(self, file) -> pd.DataFrame:
        """
        Converts CSV file to pandas dataframe
        :param file:
        :return:
        """
        pass
