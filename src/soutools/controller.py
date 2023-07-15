#controller.py
"""Controlls the main logic of the program"""

from colors import color
from consolemenu import *
from consolemenu.items import *
from consolemenu.prompt_utils import PromptUtils
import logging

logger = logging.getLogger(__name__)

MENU_TITLE = """
   ____          _   _         __  __                     _     _ 
  / ___|   ___  | | | |       |  \/  |  ___  _ __   __ _ | | __(_)
  \___ \  / _ \ | | | | _____ | |\/| | / _ \| '__| / _` || |/ /| |
   ___) || (_) || |_| ||_____|| |  | ||  __/| |   | (_| ||   < | |
  |____/  \___/  \___/        |_|  |_| \___||_|    \__,_||_|\_\|_|
"""

def select_organization():
    print("You have choosen select organization")
    PromptUtils(Screen()).enter_to_continue()

def select_network():
    print("You have choosen select network")
    PromptUtils(Screen()).enter_to_continue()

def wireless_options():
    print("You have choosen select wireless")
    PromptUtils(Screen()).enter_to_continue()

def menu():
    # Create the root menu
    menu = ConsoleMenu(MENU_TITLE, color("Main menu screen", fg='Red'), show_exit_option=False)

    # Add all the items to the root menu
    menu.append_item(FunctionItem(color("Select an organization", fg='Green'), select_organization))
    menu.append_item(FunctionItem(color("Select a network", fg='Green'), select_network))
    menu.append_item(FunctionItem(color("Go to wireless options", fg='Green'), wireless_options))
    menu.append_item(ExitItem(color("Exit program", fg='Green')))
    

    # Show the menu
    menu.start()
    menu.join()