#controller.py

"""Controlls the main logic of the program"""

import sys
from colors import color
from consolemenu import *
from consolemenu.items import *
from consolemenu.prompt_utils import PromptUtils
import logging

from soutools import model, helpers

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

def wireless_report():
    logger.debug('The "wireless_report" function called')
    if org_id:
        networks = dashboard.get_wireless_networks(org_id)
    else:
        print('No organization selected, please select organization first\n')
    path = helpers.get_settings.get_value('wireless_networks.output_file')
    helpers.writelines_to_file(path, networks)
    PromptUtils(Screen()).enter_to_continue()

def wireless_with_ssid_x_report():
    logger.debug('The "wireless_with_ssid_x_report" function called')
    dashboard.wheres_ssid_x()
    PromptUtils(Screen()).enter_to_continue()

def update_radius_settings():
    logger.debug('The "update_radius_settings" function called')
    dashboard.update_radius_servers()
    PromptUtils(Screen()).enter_to_continue()

def menu():
    logger.debug('The "menu" funciton called')
    # Create the root menu
    menu = ConsoleMenu(MENU_TITLE, color("Main menu screen", fg='Red'), show_exit_option=False)
    logger.debug('The ConsoleMenu has been instantiated')

    # Create the wireless submenu
    wireless_submenu = ConsoleMenu(MENU_TITLE, color("Wireless Submenu", fg='Red'), show_exit_option=False)
    wireless_submenu.append_item(FunctionItem(color("Generate a report of all sites of type wireless", fg='Green'), wireless_report))
    wireless_submenu.append_item(FunctionItem(color("Generate a report of all sites with a particular SSID", fg='Green'), wireless_with_ssid_x_report))
    wireless_submenu.append_item(FunctionItem(color("Update radius servers for a particular SSID", fg='Green'), update_radius_settings))
    wireless_submenu.append_item(ExitItem(color("Return to the main menu", fg='Green')))
    # Menu item for opening submenu 2
    submenu_item_2 = SubmenuItem(color("Go to wireless options", fg='Green'), submenu=wireless_submenu)
    submenu_item_2.set_menu(menu)

    # Add all the items to the root menu
    menu.append_item(FunctionItem(color("Select an organization", fg='Green'), select_organization))
    menu.append_item(FunctionItem(color("View the selected organization", fg='Green'), view_organization))
    menu.append_item(submenu_item_2)
    menu.append_item(ExitItem(color("Exit program", fg='Green')))

    # Show the menu
    menu.start()
    menu.join()
