import os
import pytest
import tomlkit

from soutools.settings import Settings


@pytest.fixture
def settings():
    return Settings("soutools/settings/settings.toml")


def test_load_settings(settings):
    # Load the settings
    settings.load_settings()

    # Assert that the settings are loaded correctly
    assert settings.get_value('default_org_id') == '123'


def test_get_value(settings):
    # Load the settings
    settings.settings = tomlkit.loads('key = "value"')

    # Assert that the value is retrieved correctly
    assert settings.get_value("key") == "value"


def test_get_value_nested(settings):
    # Load the settings
    settings.settings = tomlkit.loads('key1 = { key2 = "value" }')

    # Assert that the nested value is retrieved correctly
    assert settings.get_value("key1.key2") == "value"


def test_get_value_settings_not_loaded(settings):
    # Assert that a ValueError is raised when trying to get a value without loading the settings first
    with pytest.raises(ValueError):
        settings.get_value("key")


def test_load_settings_file_not_found(tmpdir):
    # Assert that a FileNotFoundError is raised when the settings file does not exist
    settings_file = tmpdir.join("settings.toml")
    settings = Settings(settings_file)
    with pytest.raises(FileNotFoundError):
        settings.load_settings()


def test_load_settings_invalid_toml(tmpdir):
    # Create a temporary settings file with invalid TOML syntax
    settings_file = tmpdir.join("settings1.toml")
    settings_file.write('key = value')
    settings = Settings(settings_file)
    # Assert that a ValueError is raised when loading the settings
    with pytest.raises(ValueError):
        settings.load_settings()