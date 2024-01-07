# menu.py

"""This is used to handle the menu system"""

from collections import namedtuple

from soutools import helpers


class Menu:
    def __init__(self, title, subtitle, options):
        menuitem = namedtuple("Option", ["label", "callback"])
        self._title = title
        self._subtitle = subtitle
        self._options = [menuitem(*option) for option in options]

    def display(self):
        helpers.clear_screen()
        print(self._title)
        print(f"  {self._subtitle}")
        print()
        menu_item = ""
        for i, option in enumerate(self._options, start=1):
            menu_item += helpers.colorme(f"    {str(i)} - {option.label}\n", "green")
        print(menu_item)

    def get_input(self):
        while True:
            try:
                self.display()
                selection = int(input("\n  Select an option >> "))
                if selection not in range(1, len(self._options) + 1):
                    print("\nEntry not in range, please try again: ")
                    input("Press Enter to Continue\n")
                    self.display()
                    continue
                else:
                    self.display()
                    return self._options[selection - 1].callback()
            except ValueError:
                print("\nEntry needs to be an integer, please try again: ")
                input("Press Enter to Continue\n")
                self.display()
                continue
