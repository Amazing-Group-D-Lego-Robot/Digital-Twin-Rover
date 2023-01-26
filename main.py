# ENTRY POINT FOR WHOLE SYSTEM

from controller.controller import Controller


def main():
    controller = Controller()

    # Proof of concept connection to show the twin server can send data
    #while True:
    #    controller.twin.update()


if __name__ == "__main__":
    main()
