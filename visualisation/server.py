import time

from ursinanetworking import *
from random import randint
from time import sleep

from twin.worldstate import WorldState


class TwinServer(UrsinaNetworkingServer):
    def __init__(self):
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

    def send_updated_world_state(self, world_state):
        if not isinstance(world_state, WorldState):
            raise ValueError

        twin_pos = (world_state.twin.pos[0], world_state.twin.pos[1], world_state.twin.pos[2])
        twin_rot = (world_state.twin.rot[0], world_state.twin.rot[1], world_state.twin.rot[2])

        self.broadcast("new_position", world_state.twin.__dict__)

    def update(self, world_state):
        while len(self.events_manager.events) > 0:
            self.process_net_events()

        self.send_updated_world_state(world_state)
