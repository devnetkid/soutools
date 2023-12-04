#!/usr/bin/env python3

"""Initialize logger and hand off control to the controller module"""

import logging
import os
import sys
from datetime import datetime

from soutools import controller, helpers, settings

helpers.clear_screen()


def main():
    get_settings = settings.Settings()

    # Get logging information from settings
    file_log_level = get_settings.get_value("logging.file_log_level")
    file_log_path = get_settings.get_value("logging.file_log_path")

    # Setup log path and ensure that folders exist. If not, then create them
    home_dir = os.path.expanduser("~")
    log_path = os.path.join(home_dir, file_log_path)
    helpers.setup_folder_structure(log_path)
    log_file = f"{log_path}soutools_log__{datetime.now():%Y-%m-%d_%H-%M-%S}.log"

    # Setup a basic logger
    logger = logging.getLogger("soutools")
    logger.setLevel(logging.DEBUG)

    # Setup file handler and add it to the logger
    fh = logging.FileHandler(filename=log_file)
    # Validate log level is a proper instance
    file_level = getattr(logging, file_log_level.upper(), None)
    if isinstance(file_level, int):
        fh.setLevel(level=file_level)
    else:
        error = f'Invalid value "{file_log_level}" ' "specified for file_log_level"
        error = helpers.colorme(error, "red")
        blue_text = helpers.colorme("file_log_level", "blue")
        error += f"\n  Check {blue_text} in the settings.toml"
        error += (
            '\n  Valid values are "debug", "info", "warning", '
            '"error", and "critical"'
        )
        print()
        sys.exit("  " + error)
    # create formatter and add it to the handler
    formatter = logging.Formatter(
        "%(asctime)2s - %(name)19s - %(levelname)8s - %(message)s"
    )
    fh.setFormatter(formatter)
    # add the handler to the logger
    logger.addHandler(fh)

    # create console handler and add it to the logger
    ch = logging.StreamHandler()
    ch.setLevel(level="WARNING")
    # create formatter and add it to the handler
    formatter = logging.Formatter("%(levelname)8s - %(message)s")
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)

    logger.debug("Logger initialized, calling controller menu function")
    controller.main_menu()


if __name__ == "__main__":
    main()
