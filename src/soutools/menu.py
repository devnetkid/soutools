"""This is used to handle the menu system"""

from collections import namedtuple
import platform, os

Option = namedtuple('Option', ['label', 'callback'])

class Menu:
    def __init__(self, title, options):
        self.title = title
        self._options = [Option(*option) for option in options]

    def display(self):
        self.clear_screen()
        print(f"\033[38;2;245;90;66m{self.title}\033[0m")
        string = ''
        for i, option in enumerate(self._options, start=1):
            string += f"    \033[38;2;90;200;66m{i} - {option.label}\033[0m\n"
        print(string)

    def callback(self, i):
        if i <= len(self._options):
            return self._options[i - 1].callback

    def get_input(self):
        while True:
            try:
                selection = int(input("\nOption >> "))
                print('')
                if selection not in range(1,len(self._options)+1):
                    print('\nEntry not in range, please try again: ')
                    input("Press Enter to Continue\n")
                    self.display()
                    continue
                else:
                    return self._options[selection-1].callback()
            except ValueError:
                print('\nEntry needs to be an integer, please try again: ')
                input("Press Enter to Continue\n")
                self.display()
                continue

    def clear_screen(self):
        if(platform.system().lower()=='windows'):
            cmd = 'cls'
        else:
            cmd = 'clear'
        os.system(cmd)