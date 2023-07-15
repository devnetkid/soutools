#controller.py

"""Controlls the main logic of the program"""

import sys
from colors import color
from consolemenu import *
from consolemenu.items import *
from consolemenu.prompt_utils import PromptUtils
import logging

from soutools import model

logger = logging.getLogger(__name__)


MENU_TITLE = """
   ____          _   _         __  __                     _     _ 
  / ___|   ___  | | | |       |  \/  |  ___  _ __   __ _ | | __(_)
  \___ \  / _ \ | | | | _____ | |\/| | / _ \| '__| / _` || |/ /| |
   ___) || (_) || |_| ||_____|| |  | ||  __/| |   | (_| ||   < | |
  |____/  \___/  \___/        |_|  |_| \___||_|    \__,_||_|\_\|_|
"""

dashboard = model.MerakiModel()
org_id = None
org_name = None

def select_organization():
    global org_id, org_name
    logger.debug('The "select_organization" function called')
    org_id, org_name = dashboard.select_organization()
    logger.debug(f'The selected organization ID is "{org_id}"')
    logger.debug(f'The selected organization name is "{org_name}"')
    logger.info(f'The selected organization name is "{org_name}"')

def view_organization():
    logger.debug('The "view_organization" function called')
    logger.debug("Checking if organization name is set")
    if not org_name:
        print("You have not selected an organization yet\n")
        logger.debug("Notified user that organization name is not set")
    else:
        print(f'You have choosen the "{org_name}"" organization\n')
        logger.debug(f"Notified user that organization name is set to {org_name}")
    PromptUtils(Screen()).enter_to_continue()

def wireless_options():
    print("You have choosen select wireless")
    PromptUtils(Screen()).enter_to_continue()

def menu():
    logger.debug('The "menu" funciton called')
    # Create the root menu
    menu = ConsoleMenu(MENU_TITLE, color("Main menu screen", fg='Red'), show_exit_option=False)
    logger.debug('The ConsoleMenu has been instantiated')
    # Add all the items to the root menu
    menu.append_item(FunctionItem(color("Select an organization", fg='Green'), select_organization))
    menu.append_item(FunctionItem(color("View the selected organization", fg='Green'), view_organization))
    menu.append_item(FunctionItem(color("Go to wireless options", fg='Green'), wireless_options))
    menu.append_item(ExitItem(color("Exit program", fg='Green')))
    
    # Show the menu
    menu.start()
    menu.join()
