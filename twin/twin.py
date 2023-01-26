# whole twin system, environment and all

from visualisation import server
from twin.worldstate import WorldState

from ursinanetworking import *
from random import randint
from time import sleep

Server = UrsinaNetworkingServer("localhost", 25565)


@Server.event
def onClientConnected(client):
    print(f"{client} connected !")
    print(f"Current clients: {Server.get_clients()}")

    for _ in range(0, 10):
        random_position()
        sleep(1)


@Server.event
def onClientDisconnected(client):
    print(f"{client} disconnected !")


def random_position():
    position = (randint(0, 20), 0, randint(0, 20))
    print("Position for client is", position)
    Server.broadcast("update_pos", position)


class TwinSystem:
    def __init__(self):
        # print("created a new twin system")

        self.twin_server = server
        self.worldstate = WorldState()

    def update(self, sensor_info=None, instruction=None):
        # update the rover with new instruction and sensor info
        # return new updated world state

        self.worldstate.twin.update(sensor_info, instruction, self.worldstate.environment)

        Server.process_net_events()

    def predict_next(self, n=1, instruction=None):
        # predict next n time steps of the twin model and returns them with the current environment

        return \
            self.worldstate.twin.predict_next(n=n, environment=self.worldstate.environment, instruction=instruction), \
                self.worldstate.environment.copy()
