import time

from ursinanetworking import *
from random import randint
from time import sleep

from twin.worldstate import WorldState


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

    def send_updated_world_state(self, world_state: WorldState):
        """
        Send a world state dictionary to the client
        :param world_state:
        :return:
        """
        self.broadcast("new_position", world_state.twin.__dict__)

    def update(self, world_state: WorldState):
        """
        Send the world state to clients after processing any inbound network events
        :param world_state:
        :return:
        """
        while len(self.events_manager.events) > 0:
            self.process_net_events()

        self.send_updated_world_state(world_state)
