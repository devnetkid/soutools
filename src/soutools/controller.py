#controller.py

"""Controlls the main logic of the program"""

import logging, sys

from soutools import menu, model, helpers

logger = logging.getLogger(__name__)

dashboard = model.MerakiModel()
org_id = helpers.get_settings.get_value('default_org_id')
org_name = helpers.get_settings.get_value('default_org_name')

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
    input('Press [ENTER] to continue...')

def wireless_options():
    menu_title = helpers.menu_title
    wireless_menu = menu.Menu(
    menu_title, [
    ('Generate a report of all sites of type wireless', wireless_report),
    ('Generate a report of all sites with a particular SSID', wireless_with_ssid_x_report),
    ('Update radius servers for a particular SSID', update_radius_settings),
    ('Return to the main menu', main_menu),
    ('Exit', quit)])

    while True:
        wireless_menu.display()
        wireless_menu.get_input()

def wireless_report():
    logger.debug('The "wireless_report" function called')
    if org_id:
        networks = dashboard.get_wireless_networks(org_id)
    else:
        print('No organization selected, please select organization first\n')
    path = helpers.get_settings.get_value('wireless_networks.output_file')
    helpers.writelines_to_file(path, networks)
    input('Press [ENTER] to continue...')

def wireless_with_ssid_x_report():
    logger.debug('The "wireless_with_ssid_x_report" function called')
    dashboard.wheres_ssid_x()
    input('Press [ENTER] to continue...')

def update_radius_settings():
    logger.debug('The "update_radius_settings" function called')
    dashboard.update_radius_servers()
    input('Press [ENTER] to continue...')

def quit():
    sys.exit()

def main_menu():
    menu_title = helpers.menu_title
    main_menu = menu.Menu(
    menu_title, [
    ('Select an organization', select_organization),
    ('View the selected organization', view_organization),
    ('Wireless options', wireless_options),
    ('Exit', quit)])

    while True:
        main_menu.display()
        main_menu.get_input()
