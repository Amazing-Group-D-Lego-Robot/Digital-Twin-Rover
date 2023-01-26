from ursinanetworking import *
from random import randint
from time import sleep

Server = UrsinaNetworkingServer("localhost", 25565)


class TwinServer:
    @Server.event
    def onClientConnected(self, client):
        print(f"{client} connected !")
        print(f"Current clients: {Server.get_clients()}")

        for _ in range(0, 10):
            self.random_position()
            sleep(1)

    @Server.event
    def onClientDisconnected(self, client):
        print(f"{client} disconnected !")

    def random_position(self):
        position = (randint(0, 20), 0, randint(0, 20))
        print("Position for client is", position)
        Server.broadcast("update_pos", position)

    def check_for_response(self):
        Server.process_net_events()
