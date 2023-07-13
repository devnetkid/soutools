# main.py

from soutools.settings import Settings

def main():
    print("Starting new_project")
    settings = Settings("soutools/settings/settings.toml")
    settings.load_settings()
    print(settings.get_value('wireless_networks.output_file'))


if __name__ == "__main__":
    main()
