from twin.twin_environment import TwinEnvironment


class DefaultSensor:
    def __init__(self, name: str):
        self.name = name
        self.value = 0

    def update(self, environment: TwinEnvironment):
        pass
