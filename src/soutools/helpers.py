"""This module is used to assists the other modules with functions like writting to file"""

import logging, os, sys

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


def validate_integer_in_range(end_range):
    """Prompts user to select a number within a defined range

    Args:
        end_range (int): The upper bound number that can be selected

    Returns:
        int: The selected number
    """

    while True:
        try:
            selected = int(input("\nOption >> "))
            assert selected in range(0, end_range)
        except ValueError:
            print("\tThat is not an integer!\n")
        except AssertionError:
            print(f"\n\tYou must enter a number between 0 and {end_range-1}")
        else:
            break
    return selected


def progress_bar_1(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(f'\rProgress |{bar}| {percent:.2f}% Complete', end='\r')


def new_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='>'):
    percent = ('{0:.}' + str(decimals) + 'f}').format(100 * (iteration/float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()


# Print iterations progress
def progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print('\n\n')


def clear_line(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)


def colorme(msg, color):
    reset = '\033[0m'
    if color == 'red':
        decoration = '\033[31m'
    elif color == 'green':
        decoration = '\033[32m'
    elif color == 'blue':
        decoration = '\033[94m'
    elif color == 'yellow':
        decoration = '\033[93m'
    else:
        raise ValueError('Invalid color')
    return decoration + msg + reset


# asci art generated by
# https://patorjk.com/software/taag/ using formatting "standard"

menu_title = """
   ____        _   _ _____           _     
  / ___|  ___ | | | |_   _|__   ___ | |___ 
  \___ \ / _ \| | | | | |/ _ \ / _ \| / __|
   ___) | (_) | |_| | | | (_) | (_) | \__ \\
  |____/ \___/ \___/  |_|\___/ \___/|_|___/
"""
