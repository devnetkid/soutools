# helpers.py

"""This module is used to assists the other modules with functions like writting to file"""

import logging
import os
import platform
import sys

from soutools import settings

logger = logging.getLogger(__name__)
get_settings = settings.Settings()
home_dir = os.path.expanduser("~")


def setup_folder_structure(path):
    logger.debug('The "setup_folder_structure" function called')
    logger.debug(f"Checking the path {path} for existance and creating if not exists")
    temp_path = os.path.split(path)
    path = temp_path[0]
    if not os.path.exists(path):
        logger.debug(f"making directory structure for {path}")
        os.makedirs(path)


def writelines_to_file(path, text):
    logger.debug('The "writelines_to_file" function called')
    # Find users home directory and join with settings location
    location = os.path.join(home_dir, path)
    logger.debug(f"The path for writelines_to_file is {location}")
    setup_folder_structure(location)

    # Write text to given path
    try:
        with open(location, "w") as file_data:
            file_data.writelines(text)
    except FileNotFoundError:
        logger.error(f"Could not open {location}")
        sys.exit()


def validate_integer_in_range(end_range):
    """Prompts user to select a number within a defined range

    Args:
        end_range (int): The upper bound number that can be selected

    Returns:
        int: The selected number
    """

    while True:
        try:
            selected = int(input("\n  Select an option >> "))
            assert selected in range(1, end_range + 1)
        except ValueError:
            print("\tThat is not an integer!\n")
        except AssertionError:
            print(f"\n\tYou must enter a number between 1 and {end_range}")
        else:
            break
    return selected - 1


def get_networks_list(path):
    filepath = os.path.join(home_dir, path)
    networks = []
    try:
        with open(filepath, "r") as netdata:
            for line in netdata:
                if not line.isspace():
                    networks.append(line.strip())
        return networks
    except FileNotFoundError:
        logger.error(f"Could not open {path}")
        sys.exit()


def format_radius():
    # Retrieve settings
    radius = get_settings.get_value("radius_servers")
    accounting = get_settings.get_value("radius_accounting")
    radius_port = radius["port"]
    radius_secret = radius["secret"]
    accounting_port = accounting["port"]
    accounting_secret = accounting["secret"]
    # Initialize payloads
    radius_payload = []
    accounting_payload = []
    # Format Radius settings
    if radius_port and radius_secret:
        for server in radius["servers"]:
            temp = {"host": server, "port": radius_port, "secret": radius_secret}
            radius_payload.append(temp)
    else:
        for server in radius["servers"]:
            server_info = server.split(";")
            temp = {
                "host": server_info[0],
                "port": int(server_info[1]),
                "secret": server_info[2],
            }
            radius_payload.append(temp)
    # Format Accounting settings
    if accounting_port and accounting_secret:
        for server in accounting["servers"]:
            temp = {
                "host": server,
                "port": accounting_port,
                "secret": accounting_secret,
            }
            accounting_payload.append(temp)
    else:
        for server in accounting["servers"]:
            server_info = server.split(";")
            temp = {
                "host": server_info[0],
                "port": int(server_info[1]),
                "secret": server_info[2],
            }
            accounting_payload.append(temp)
    # Return the formatted payloads
    return radius_payload, accounting_payload


def progress_bar(progress, total, width=40):
    char = chr(9632)
    logger.debug(f"progress is {progress}")
    logger.debug(f"total is {total}")
    if progress >= total:
        logger.debug("finished has been set to true")
        fill_char = colorme(char, "green")
    else:
        fill_char = colorme(char, "red")
    completed = int(width * (progress / total))
    bar = "Progress: [" + fill_char * completed + "-" * (width - completed) + "] "
    percent_done = round(progress / total * 100, 1)
    bar += str(percent_done) + "% " + str(progress) + "/" + str(total)
    return bar


def colorme(msg, color):
    if color == "red":
        wrapper = "\033[91m"
    elif color == "blue":
        wrapper = "\033[94m"
    elif color == "green":
        wrapper = "\033[92m"
    else:
        # Defaults to white if invalid color is given
        wrapper = "\033[47m"
    return wrapper + msg + "\033[0m"


def clear_screen():
    if platform.system().lower() == "windows":
        cmd = "cls"
    else:
        cmd = "clear"
    os.system(cmd)


# https://patorjk.com/software/taag/ using font "standard"

menu_title = colorme(
    r"""
   ____        _   _ _____           _
  / ___|  ___ | | | |_   _|__   ___ | |___
  \___ \ / _ \| | | | | |/ _ \ / _ \| / __|
   ___) | (_) | |_| | | | (_) | (_) | \__ \
  |____/ \___/ \___/  |_|\___/ \___/|_|___/
""",
    "red",
)
