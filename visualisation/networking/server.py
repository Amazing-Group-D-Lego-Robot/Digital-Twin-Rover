import time

from ursinanetworking import *
from random import randint
from time import sleep

from twin.twin_model import TwinModel


class TwinServer(UrsinaNetworkingServer):
    """
    Class to override UrsinaNetworkingClient from UrsinaNetworking
    """
    def __init__(self):
        """
        Override UrsinaNetworking constants for PEP8 conformity
        """
        super().__init__("localhost", 25565)
        ursinanetworking.BUILTIN_EVENT_CLIENT_CONNECTED = 'on_client_connected'
        ursinanetworking.BUILTIN_EVENT_CLIENT_DISCONNECTED = 'on_client_disconnected'

        @self.event
        def on_client_connected(client):
            print(f"{client} connected !")
            print(f"Current clients: {self.get_clients()}")

        @self.event
        def on_client_disconnected(client):
            print(f"{client} disconnected !")

    def send_updated_world_state(self, twin: TwinModel, environment):
        """
        Send a world state dictionary to the client
        :param twin:
        :param environment:
        :return:
        """

        self.broadcast("new_position", twin.get_sensors_and_properties())

    def update(self, twin, environment):
        """
        Send the world state to clients after processing any inbound network events
        :param twin:
        :param environment:
        :return:
        """
        while len(self.events_manager.events) > 0:
            self.process_net_events()

        self.send_updated_world_state(twin, environment)
