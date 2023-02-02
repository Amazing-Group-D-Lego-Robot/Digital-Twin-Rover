from ursinanetworking import *


class VisualClient(UrsinaNetworkingClient):
    """
    Class to override UrsinaNetworkingClient from UrsinaNetworking, needed to allow graceful close
    """
    def __init__(self):
        """
        Override UrsinaNetworking constants for PEP8 conformity
        """
        super().__init__("localhost", 25565)
        ursinanetworking.BUILTIN_EVENT_CONNECTION_ETABLISHED = "on_connected"
        ursinanetworking.BUILTIN_EVENT_CONNECTION_ERROR = "on_disconnected"

        @self.event
        def on_connected():
            print("I'm connected to the server!")

        @self.event
        def on_disconnected(reason):
            self.close()
            quit()

    def close(self):
        """
        Close the local client socket which causes a cascading error through running threads which closes the client
        :return:
        """
        ursina_networking_log("UrsinaNetworkingClient", "close", f"Closing client connections")
        self.client.close()
