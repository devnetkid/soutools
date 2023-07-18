import os
import tomlkit


class Settings:
    # In a future release will add ability to specify the path when running app
    def __init__(self, file_name='soutools/settings/settings.toml'):
        self.file_name = file_name
        self.settings = None
        self.load_settings()

    def load_settings(self):
        home_dir = os.path.expanduser("~")
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
                raise ValueError(f"Wasn't able to create default config file at location {settings_path}")


        try:
            with open(settings_path, "r") as file:
                self.settings = tomlkit.loads(file.read())
        except tomlkit.exceptions.TOMLKitError as e:
            raise ValueError(f"Error decoding TOML file: {str(e)}")

    def get_value(self, key):
        if self.settings is None:
            raise ValueError("Settings have not been loaded. Call load_settings() first.")

        keys = key.split('.')
        value = self.settings
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None

        return value


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

[radius_servers]
servers = [
"radius1.company.com",
"radius2.company.com",
"radius3.company.com"]
port = 1812
secret = "mySecret"

[radius_accounting]
servers = [
"radius1.company.com",
"radius2.company.com",
"radius3.company.com"]
port = 1813
secret = "mySecret"

# Overall settings
[logging]
file_log_level = 'info'
file_log_path = 'soutools/output/logs/'
log_to_console = true
console_log_level = 'info'

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