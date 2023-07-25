# settings.py

"""Used to create settings file if not exists and get settings"""

import os

import tomlkit


class Settings:
    # In a future release will add ability to specify the path when running app
    def __init__(self, file_name='soutools/settings/settings.toml'):
        self.file_name = file_name
        self.settings = None
        self.load_settings()


    def load_settings(self):
        home_dir = os.path.expanduser('~')
        settings_path = os.path.join(home_dir, self.file_name)

        if not os.path.exists(settings_path):
            #Create path and copy default settings.toml into it
            temp = os.path.split(settings_path)
            os.makedirs(temp[0])
            default_settings = tomlkit.loads(toml_template)
            try:
                with open(settings_path, 'w') as toml_data:
                    toml_data.write(tomlkit.dumps(default_settings))
            except FileNotFoundError:
                raise ValueError(f'Wasn\'t able to create default config file at location {settings_path}')
        try:
            with open(settings_path, 'r') as file:
                self.settings = tomlkit.loads(file.read())
        except tomlkit.exceptions.TOMLKitError as e:
            raise ValueError(f'Error decoding TOML file: {str(e)}')


    def get_value(self, key):
        if self.settings is None:
            raise ValueError('Settings have not been loaded. Call load_settings() first.')

        keys = key.split('.')
        value = self.settings
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None

        return value


# This is used to create a default template for the settings.toml file
toml_template = """# settings.toml

default_org_id = ''
default_org_name = ''

# Section 3.1 settings 
# Generate a report of all sites of type wireless
[wireless_networks]
output_file = 'soutools/input/wireless.txt'

# Section 3.2 settings
# Generate a report of all sites with a particular SSID
[networks_with_ssid]
ssid = 'yourSSID'
input_file = 'soutools/input/wireless.txt'
output_file = 'soutools/output/myssid.txt'

# Section 3.3 settings
#Update radius servers for a particular SSID
[radius]
input_file = 'soutools/output/myssid.txt'

#------------------------------------------------------------------------------------#
# For both radius and accounting servers you can use any of the following formats:
# First format looks like this... (where the values are seperated by a semicolon)
#   servers = ['radius1.com;1812;firstSecret','radius2.com;1912;secondSecret']
#   ports = ''
#   secret = ''
# if using this format leave port and secret set as empty strings.
#
# The second format is for when the port and secret are the same for either
# the radius or accounting servers.
# Second scenario would like this...
#   servers = ['radius1.com','radius2.com']
#   port = 1812
#   secret = 'mysecret'
#------------------------------------------------------------------------------------#

[radius_servers]
servers = [
'radius1.company.com;1812;firstSecret',
'radius2.company.com;1912;secondSecret',
'radius3.company.com;2012;thirdSecret']
port = ''
secret = ''

[radius_accounting]
servers = [
'radius1.company.com',
'radius2.company.com',
'radius3.company.com']
port = 1813
secret = 'mySecret'

# Overall settings
[logging]
file_log_level = 'info'
file_log_path = 'soutools/output/logs/'

# Spefic to the meraki library
[meraki]
api_key = false
api_key_environment_variable = 'MERAKI_DASHBOARD_API_KEY'
suppress_logging = true
print_to_console = false
output_log = true
log_file_prefix = 'meraki_api_'
log_path = 'sou_meraki/output/logs'
"""