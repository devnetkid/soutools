# main.py
"""Initialize logger and hand off control to the controller module"""

from datetime import datetime
import logging
import os

from soutools import settings, controller, helpers

def main():
    get_settings = settings.Settings()

    # Get logging information from settings
    file_log_level = get_settings.get_value('logging.file_log_level')
    file_log_path = get_settings.get_value('logging.file_log_path')
    log_to_console = get_settings.get_value('logging.log_to_console')
    console_log_level = get_settings.get_value('logging.console_log_level')

    # Setup log path and ensure that folders exist and if not, then create them
    home_dir = os.path.expanduser("~")
    log_path = os.path.join(home_dir, file_log_path)
    helpers.setup_folder_structure(log_path)
    log_file = f'{log_path}soutools_log__{datetime.now():%Y-%m-%d_%H-%M-%S}.log'

    # Setup a basic logger
    logger = logging.getLogger('soutools')
    logger.setLevel(logging.DEBUG)

    # Setup file handler and add it to the logger
    fh = logging.FileHandler(filename=log_file)
    # Validate log level is a proper instance
    file_level = getattr(logging, file_log_level.upper(), None)
    if not isinstance(file_level, int):
        raise ValueError('Invalid log level: %s' % file_log_level)
    else:
        fh.setLevel(level = file_level)
    # create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)2s - %(name)19s - %(levelname)8s - %(message)s')
    fh.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)

    # create console handler and add it to the logger
    if log_to_console:
        ch = logging.StreamHandler()
                # Validate log level is a proper instance
        console_level = getattr(logging, console_log_level.upper(), None)
        if not isinstance(console_level, int):
            raise ValueError('Invalid log level: %s' % console_log_level)
        else:
            ch.setLevel(level = console_level)
        # create formatter and add it to the handler
        formatter = logging.Formatter('%(levelname)8s - %(message)s')
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(ch)
    
    logger.debug("Logger initialized, calling controller menu")
    controller.main_menu()


if __name__ == "__main__":
    main()
