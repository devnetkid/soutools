#controller.py
"""Controlls the main logic of the program"""

import logging
logger = logging.getLogger(__name__)

def test_logging():
    logger.debug("This is a debug from the controller")
    logger.info("This is a info from the controller")
    logger.warning("This is a warning from the controller")
    logger.error("This is an error from the controller")
    logger.critical("This is an critical from the controller")