# ENTRY POINT FOR WHOLE SYSTEM
from menu.main_menu import MainMenu
import logging


def main():
    # Logging handler
    log_level = logging.INFO

    # Instantiate logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # define handler and formatter
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    # add formatter to handler
    handler.setFormatter(formatter)

    # add handler to logger
    logger.addHandler(handler)

    logging.basicConfig(level=log_level, format='%(asctime)s :: %(levelname)s :: %(message)s')

    menu = MainMenu()
    menu.launch()


if __name__ == "__main__":
    main()
