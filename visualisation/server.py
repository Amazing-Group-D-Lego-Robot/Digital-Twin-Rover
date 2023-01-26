from ursinanetworking import *
from random import randint
from time import sleep

from twin.worldstate import WorldState


class TwinServer:
    def __init__(self):
        self.server = UrsinaNetworkingServer("localhost", 25565)

        @self.server.event
        def onClientConnected(client):
            print(f"{client} connected !")
            print(f"Current clients: {self.server.get_clients()}")

        @self.server.event
        def onClientDisconnected(client):
            print(f"{client} disconnected !")

    def random_position(self):
        position = (randint(0, 20), 0, randint(0, 20))
        print("Position for client is", position)
        self.server.broadcast("update_pos", position)

    def send_updated_world_state(self, world_state):
        if not isinstance(world_state, WorldState):
            raise ValueError

        twin_pos = (world_state.twin.x_pos, world_state.twin.y_pos, world_state.twin.z_pos)
        twin_rot = (world_state.twin.x_rot, world_state.twin.y_rot, world_state.twin.z_rot)

        self.server.broadcast("update_twin_pos", twin_pos)
        self.server.broadcast("update_twin_rot", twin_rot)

    def update(self, world_state):
        while len(self.server.events_manager.events) > 0:
            self.server.process_net_events()

        self.send_updated_world_state(world_state)


