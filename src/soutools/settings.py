import os
import tomlkit


class Settings:
    def __init__(self, file_name='soutools/settings/settings.toml'):
        self.file_name = file_name
        self.settings = None
        self.load_settings()

    def load_settings(self):
        home_dir = os.path.expanduser("~")
        settings_path = os.path.join(home_dir, self.file_name)

        if not os.path.exists(settings_path):
            raise FileNotFoundError(f"settings file '{self.file_name}' not found in the home directory.")

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