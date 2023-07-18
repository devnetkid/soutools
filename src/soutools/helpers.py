# helpers.py

"""This module is used to assists the other modules with functions like writting to file"""

import logging
import os, sys
from soutools import settings

logger = logging.getLogger(__name__)

get_settings = settings.Settings()
home_dir = os.path.expanduser("~")

def setup_folder_structure(path):
    logger.debug('The "setup_folder_structure" function called')
    logger.debug(f'Checking the path {path} for existance and creating if not exists')
    temp_path = os.path.split(path)
    path = temp_path[0]
    if not os.path.exists(path):
        logger.debug(f'making directory structure for {path}')
        os.makedirs(path)


def writelines_to_file(path, text):
    logger.debug('The "writelines_to_file" function called')
    # Find users home directory and join with settings location
    location = os.path.join(home_dir, path)
    logger.debug(f'The path for writelines_to_file is {location}')
    setup_folder_structure(location)
    
    # Write text to given path
    try:
        with open(location, 'w') as file_data:
            file_data.writelines(text)
    except FileNotFoundError:
        logger.error(f'Could not open {location}')
        sys.exit()


def get_networks_list(path):
    filepath = os.path.join(home_dir, path)
    try:
        with open(filepath, 'r') as netdata:
            networks = netdata.readlines()
        return networks
    except FileNotFoundError:
        logger.error(f'Could not open {path}')
        sys.exit()        


def format_radius():
    radius = get_settings.get_value('radius_servers')
    accounting = get_settings.get_value('radius_accounting')
    radius_port = radius['port']
    radius_secret = radius['secret']
    accounting_port = accounting['port']
    accounting_secret = accounting['secret']

    radius_payload = []
    accounting_payload = []

    # Format Radius settings
    for server in radius['servers']:
        temp = {'host':server, 'port':radius_port, 'secret':radius_secret}
        radius_payload.append(temp)
    # Format Radius Accounting settings
    for server in accounting['servers']:
        temp = {'host':server, 'port':accounting_port, 'secret':accounting_secret}
        accounting_payload.append(temp)

    return radius_payload, accounting_payload


# https://patorjk.com/software/taag/ using formatting "standard"

menu_title = """
   ____        _   _ _____           _     
  / ___|  ___ | | | |_   _|__   ___ | |___ 
  \___ \ / _ \| | | | | |/ _ \ / _ \| / __|
   ___) | (_) | |_| | | | (_) | (_) | \__ \\
  |____/ \___/ \___/  |_|\___/ \___/|_|___/
"""
