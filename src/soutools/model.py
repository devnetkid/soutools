#!/usr/bin/env python3

"""This module handles the interface between the controller and the Meraki Dashboard
"""

import logging
import os
import sys

import meraki

from soutools import helpers

logger = logging.getLogger(__name__)

logger.info("Loading settings for the dashboard instance")


class MerakiModel:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        logger.info("Instantiated an instance of the model.MerakiModel class")
        if helpers.get_settings.get_value('meraki.API_KEY'):
            api_key = helpers.get_settings.get_value('meraki.API_KEY')
        elif helpers.get_settings.get_value('meraki.API_KEY_ENVIRONMENT_VARIABLE') in os.environ:
            api_key = os.environ.get(helpers.get_settings.get_value('meraki.API_KEY_ENVIRONMENT_VARIABLE'))
        else:
            logger.error("API Key not found")
            sys.exit("ERROR: API Key not found")


        # Instantiate an instance of the Meraki dashboard
        self.dashboard = meraki.DashboardAPI(
            api_key=api_key,
            output_log=helpers.get_settings.get_value('meraki.OUTPUT_LOG'), 
            print_console=helpers.get_settings.get_value('meraki.PRINT_TO_CONSOLE'), 
            suppress_logging=helpers.get_settings.get_value('meraki.SUPPRESS_LOGGING'),
            log_file_prefix=helpers.get_settings.get_value('meraki.LOG_FILE_PREFIX'),
            log_path=helpers.get_settings.get_value('meraki.LOG_PATH')
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


    def get_wireless_networks(self, organization_id):
        logger.debug(f'The "get_wireless_networks" function called with org_id {organization_id}')
        networks = self.dashboard.organizations.getOrganizationNetworks(
        organization_id, total_pages='all')
        wireless = 0
        no_wireless = 0
        wireless_networks = []
        for network in networks:
            if 'wireless' in network['productTypes']:
                wireless_networks.append(network['id'] + ',' + network['name'] + '\n')
                logger.info(f'network {network["name"]}, was identified as having some type of wireless')
                wireless += 1
            else:
                logger.info(f'network {network["name"]}, was identified as not having some type of wireless')
                no_wireless += 1
        
        logger.info(f"INFO: There are {wireless} sites with some type of wireless device")
        logger.info(f"INFO: There were {no_wireless} sites with no wireless")
        
        return wireless_networks


    def wheres_ssid_x(self):
        logger.debug('The "wheres_ssid" function called')
        search_ssid = helpers.get_settings.get_value('networks_with_ssid.ssid')
        input_file = helpers.get_settings.get_value('networks_with_ssid.input_file')
        networks = helpers.get_networks_list(input_file)
        path = helpers.get_settings.get_value('networks_with_ssid.output_file')
        logger.debug(f'We are searching for ssid "{search_ssid}"')
        logger.debug(f'We are searching for networks found in "{input_file}"')
        logger.debug(f'We are writting to the path "{path}"')
        found_count = not_found_count = 0 
        ssid_sites = []
        for network in networks:
            site = network.split(',')
            site_id = site[0]
            site_name = site[1].strip('\n')
            logger.debug(f'Calling Meraki dashboard to pull all SSIDs for network {site_id}')
            ssids = self.dashboard.wireless.getNetworkWirelessSsids(site_id)
            found_ssid = False
            for ssid in ssids:
                if (ssid['name'] == search_ssid and ssid['enabled'] == True and ssid['authMode'] == "8021x-radius"):
                    found_ssid = True
                    newline = f"{site_id},{site_name},{ssid['name']},{ssid['number']}\n"
                    ssid_sites.append(newline)
                    logger.info(f'Found SSID {search_ssid} for "{site_name}"')
                    found_count += 1
            if not found_ssid:
                logger.info(f'SSID {search_ssid} was not found for "{site_name}"')
                not_found_count += 1
        helpers.writelines_to_file(path, ssid_sites)
        logger.info(f"Sites with SSID {search_ssid}, found {found_count}")
        logger.info(f"Sites without SSID {search_ssid}, found {not_found_count}")


    def update_radius_servers(self):
        logger.debug('The "update_radius_servers" function called')
        input_file = helpers.get_settings.get_value('radius.input_file')
        networks = helpers.get_networks_list(input_file)
        radius, accounting = helpers.format_radius()
        logger.debug(f'We are searching for networks "{networks}"')
        logger.debug(f'We are searching for radius servers "{radius}"')
        logger.debug(f'We are searching for accounting servers "{accounting}"')
        
        counter = 0
        for network in networks:
            site = network.split(',')
            net_id = site[0]
            net_name = site[1]
            ssid_num = site[3].strip('\n')
            logger.info(f'Updating radius settings for {net_name} and SSID number {ssid_num}')
            logger.debug(f'Calling Meraki dashboard with {net_id} {ssid_num} {radius} {accounting}')
        #    self.dashboard.wireless.updateNetworkWirelessSsid(
        #        networkId=net_id,
        #        number=ssid_num, 
        #        radiusServers=radius,
        #        radiusAccountingServers=accounting
        #    )
            counter += 1
        logger.info(f'Updated radius settings on {counter} SSIDs')
