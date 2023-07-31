# controller.py

"""Controlls the main logic of the program"""

import logging
import sys

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
    logger.info(f'The selected organization name is "{org_name}"')


def view_organization():
    logger.debug('The "view_organization" function called')
    logger.debug('Checking if organization name is set')
    if not org_name:
        print('\nYou have not selected an organization yet\n')
        logger.debug('Notified user that organization name is not set')
    else:
        highlight_orgname = helpers.colorme(org_name, 'blue')
        highlight_orgid = helpers.colorme(org_id, 'blue')
        print(f'\nThe "{highlight_orgname}" organization with ID {highlight_orgid} is currently selected\n')
        logger.debug(f'Notified user that organization name is set to {org_name}')
    input('Press [ENTER] to continue...')


def wireless_options():
    menu_title = helpers.menu_title
    wireless_menu = menu.Menu(
    menu_title, [
    ('Generate a report of all sites of type wireless', wireless_report),
    ('Generate a report of all sites with a particular SSID', wireless_report_with_ssid_number),
    ('Update radius servers for a particular SSID', update_radius_settings),
    ('Return to the main menu', main_menu),
    ('Exit', quit)])
    while True:
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


def wireless_report_with_ssid_number():
    logger.debug('The "wireless_with_ssid_x_report" function called')
    dashboard.find_ssid_number()
    input('Press [ENTER] to continue...')


def update_radius_settings():
    make_changes = 'n'
    logger.debug('The "update_radius_settings" function called')
    warning = helpers.colorme('WARNING', 'red')
    highlight_orgname = helpers.colorme(org_name, 'blue')
    print(f'{warning} - You are about to make changes to the {highlight_orgname} organizaiton')
    make_changes = input('Are you sure you want to continue [Y/N] ').upper()
    if 'Y' in make_changes:
        print()
        dashboard.update_radius_servers()
        input('Press [ENTER] to continue...')
    else:
        wireless_options()
    


def quit():
    helpers.clear_screen()
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
        main_menu.get_input()
