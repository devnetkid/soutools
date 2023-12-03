# controller.py

"""Controlls the main logic of the program"""

import logging
import sys

from soutools import helpers, menu, model

logger = logging.getLogger(__name__)
dashboard = model.MerakiModel()
org_id = helpers.get_settings.get_value('default_org_id')
org_name = helpers.get_settings.get_value('default_org_name')
net_id = helpers.get_settings.get_value('default_net_id')
net_name = helpers.get_settings.get_value('default_net_name')


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
        print(f'\nThe "{highlight_orgname}" organization with ID'\
            f' {highlight_orgid} is currently selected\n')
        logger.debug(f'Notified user that organization name is set to {org_name}')
    input('Press [ENTER] to continue...')


def select_network():
    global net_id, net_name
    logger.debug('The "select_network" function called')
    # Make sure org has been defined as network depends on it
    if not org_id:
        print('Please choose an organization first')
        input('Press [ENTER] to continue...')
    else:
        net_id, net_name = dashboard.select_network(org_id)
        if net_id:
            logger.debug(f'The selected network ID is "{net_id}"')
            logger.info(f'The selected network name is "{net_name}"')
        else:
            input('Press [ENTER] to continue...')


def view_network():
    logger.debug('The "view_network" function called')
    logger.debug('Checking if network name is set')
    if not net_name:
        print('\nYou have not selected a network yet\n')
        logger.debug('Notified user that network name is not set')
    else:
        highlight_netname = helpers.colorme(net_name, 'blue')
        highlight_netid = helpers.colorme(net_id, 'blue')
        print(f'\nThe "{highlight_netname}" network with ID'\
            f' {highlight_netid} is currently selected\n')
        logger.debug(f'Notified user that network name is set to {net_name}')
    input('Press [ENTER] to continue...')


def policy_options():
    menu_title = helpers.menu_title
    policy_menu = menu.Menu(
    menu_title, [
    ('Check a site for existing group policies', policy_report),
    ('View a particular group policy for a site', policy_view),
    ('Create a group policy', policy_create),
    ('Delete a particular group policy', policy_delete),
    ('Return to the main menu', main_menu),
    ('Exit', quit)])
    while True:
        policy_menu.get_input()


def policy_report():
    logger.debug('The "policy_report" function called')
    # Requires the network ID be set
    if not net_id:
        print('\nYou have not selected a network yet\n')
        logger.debug('Notified user that network name is not set')
    else:
        dashboard.get_group_policies(net_id)
        print()
    input('Press [ENTER] to continue...')


def policy_view():
    logger.debug('The "policy_view" function called')
    # Requires the network ID be set
    if not net_id:
        print('\nYou have not selected a network yet\n')
        logger.debug('Notified user that network name is not set')
    else:
        result = dashboard.view_group_policy(net_id)
        if not result:
            print("Specified policy was not found")
    input('\nPress [ENTER] to continue...')


def policy_create():
    logger.debug('The "policy_create" function called')
    warning = helpers.colorme('WARNING', 'red')
    highlight_orgname = helpers.colorme(org_name, 'blue')
    print(f'{warning} - You are about to make changes to the {highlight_orgname} organizaiton')
    make_changes = input('Are you sure you want to continue [Y/N] ').upper()
    if 'Y' in make_changes:
        print()
        dashboard.create_group_policy()
        input('Press [ENTER] to continue...')
    else:
        policy_options()


def policy_delete():
    logger.debug('The "policy_delete" function called')
    # Requires the network ID be set
    if not net_id:
        print('\nYou have not selected a network yet\n')
        logger.debug('Notified user that network name is not set')
        input('Press [ENTER] to continue...')
    else:
        warning = helpers.colorme('WARNING', 'red')
        highlight_orgname = helpers.colorme(org_name, 'blue')
        print(f'{warning} - You are about to make changes to the {highlight_orgname} organizaiton')
        make_changes = input('Are you sure you want to continue [Y/N] ').upper()
        if 'Y' in make_changes:
            print()
            result = dashboard.delete_group_policy(net_id)
            if not result:
                warning = helpers.colorme('WARNING', 'red')
                print(f"{warning} Failed to delete the specified policy.")
                print("Please confirm that the name is correct and try again.")
            input('Press [ENTER] to continue...')
        else:
            policy_options()


def wireless_options():
    menu_title = helpers.menu_title
    wireless_menu = menu.Menu(
    menu_title, [
    ('Generate a report of all sites of type wireless', wireless_report),
    ('Generate a report of all sites with a particular SSID', wireless_report_with_ssid_number),
    ('Update radius servers for a particular SSID', update_radius_settings),
    ('Enable/Disable all sites with a particular SSID', enable_disable_ssid),
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
    

def enable_disable_ssid():
    ssid = helpers.get_settings.get_value('networks_with_ssid.ssid')
    menu_title = helpers.menu_title
    main_menu = menu.Menu(
    menu_title, [
    (f'Enable ssid "{ssid}" in the "{org_name}" org', enable_sites_with_ssid),
    (f'Disable ssid "{ssid}" in the "{org_name}" org', disable_sites_with_ssid),
    ('Return to wireless options', wireless_options),
    ('Exit', quit)])
    while True:
        main_menu.get_input()


def enable_sites_with_ssid():
    make_changes = 'n'
    logger.debug('The "enable_sites_with_ssid" function called')
    warning = helpers.colorme('WARNING', 'red')
    highlight_orgname = helpers.colorme(org_name, 'blue')
    print(f'{warning} - You are about to make changes to the {highlight_orgname} organizaiton')
    make_changes = input('Are you sure you want to continue [Y/N] ').upper()
    if 'Y' in make_changes:
        print()
        dashboard.enable_disable_paticular_ssid(True)
        input('Press [ENTER] to continue...')
    else:
        enable_disable_ssid()


def disable_sites_with_ssid():
    make_changes = 'n'
    logger.debug('The "enable_sites_with_ssid" function called')
    warning = helpers.colorme('WARNING', 'red')
    highlight_orgname = helpers.colorme(org_name, 'blue')
    print(f'{warning} - You are about to make changes to the {highlight_orgname} organizaiton')
    make_changes = input('Are you sure you want to continue [Y/N] ').upper()
    if 'Y' in make_changes:
        print()
        dashboard.enable_disable_paticular_ssid(False)
        input('Press [ENTER] to continue...')
    else:
        enable_disable_ssid()


def quit():
    helpers.clear_screen()
    sys.exit()


def main_menu():
    menu_title = helpers.menu_title
    main_menu = menu.Menu(
    menu_title, [
    ('Select an organization', select_organization),
    ('View the selected organization', view_organization),
    ('Select a network', select_network),
    ('View the selected network', view_network),
    ('Group Policy options', policy_options),
    ('Wireless options', wireless_options),
    ('Exit', quit)])
    while True:
        main_menu.get_input()
