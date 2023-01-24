from ursinanetworking import *
from random import randint
from time import sleep

Server = UrsinaNetworkingServer("localhost", 25565)


@Server.event
def onClientConnected(Client):
    print(f"{Client} connected !")
    print(f"Current clients: {Server.get_clients()}")

    for _ in range(0, 10):
        random_position()
        sleep(1)


@Server.event
def onClientDisconnected(Client):
    print(f"{Client} disconnected !")


def random_position():
    position = (randint(0, 20), 0, randint(0, 20))
    print("Position for client is", position)
    Server.broadcast("update_pos", position)


# clients = Server.get_clients_ids()
while True:
    Server.process_net_events()
