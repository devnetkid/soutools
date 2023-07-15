#!/usr/bin/env python3

"""This module handles the interface between the controller and the Meraki Dashboard
"""

import logging
import os
import sys

import meraki

from soutools import settings

logger = logging.getLogger(__name__)

logger.info("Loading settings for the dashboard instance")
get_settings = settings.Settings()


class MerakiModel:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        logger.info("Instantiated an instance of the model.MerakiModel class")
        if get_settings.get_value('meraki.API_KEY'):
            api_key = get_settings.get_value('meraki.API_KEY')
        elif get_settings.get_value('meraki.API_KEY_ENVIRONMENT_VARIABLE') in os.environ:
            api_key = os.environ.get(get_settings.get_value('meraki.API_KEY_ENVIRONMENT_VARIABLE'))
        else:
            logger.error("API Key not found")
            sys.exit("ERROR: API Key not found")


        # Instantiate an instance of the Meraki dashboard
        self.dashboard = meraki.DashboardAPI(
            api_key=api_key,
            output_log=get_settings.get_value('meraki.OUTPUT_LOG'), 
            print_console=get_settings.get_value('meraki.PRINT_TO_CONSOLE'), 
            suppress_logging=get_settings.get_value('meraki.SUPPRESS_LOGGING'),
            log_file_prefix=get_settings.get_value('meraki.LOG_FILE_PREFIX'),
            log_path=get_settings.get_value('meraki.LOG_PATH')
        )


    def select_organization(self):
        """Lists all organizations and prompts the user to select one

        Args:
            dashboard (obj): The Meraki dashboard instance

        Returns:
            str: the selected organization ID
            str: the selected organization name
        """
        logger.debug('The "select_organization" function called from the model')
        organizations = None
        try:
            logger.debug("Trying to get organizations from the Meraki dashboard")
            organizations = self.dashboard.organizations.getOrganizations()
            logger.debug(f"organizations is equal to {organizations}")
        except meraki.exceptions.APIError:
            sys.exit("Check network connection and/or DNS settings.")
        counter = 0
        print("\nSelect organization:\n")
        for organization in organizations:
            name = organization["name"]
            print(f"{counter} - {name}")
            counter += 1
        selected = int(input("\nMake a choice: ")) # misc.validate_integer_in_range(counter)
        return (
            organizations[int(selected)]["id"],
            organizations[int(selected)]["name"]
        )


