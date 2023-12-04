# model.py

"""This module handles the interface between the controller and the Meraki Dashboard"""

import json
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
        if helpers.get_settings.get_value("meraki.api_key"):
            api_key = helpers.get_settings.get_value("meraki.api_key")
        elif (
            helpers.get_settings.get_value("meraki.api_key_environment_variable")
            in os.environ
        ):
            api_key = os.environ.get(
                helpers.get_settings.get_value("meraki.api_key_environment_variable")
            )
        else:
            logger.error("API Key not found")
            sys.exit("ERROR: API Key not found")

        # Instantiate an instance of the Meraki dashboard
        self.dashboard = meraki.DashboardAPI(
            api_key=api_key,
            output_log=helpers.get_settings.get_value("meraki.output_log"),
            print_console=helpers.get_settings.get_value("meraki.print_to_console"),
            suppress_logging=helpers.get_settings.get_value("meraki.suppress_logging"),
            log_file_prefix=helpers.get_settings.get_value("meraki.log_file_prefix"),
            log_path=helpers.get_settings.get_value("meraki.log_path"),
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
            sys.exit("Check network settings and verify API Key")
        organizations.sort(key=lambda x: x["name"])
        print("  Organizations to choose from:\n")
        for line_num, organization in enumerate(organizations, start=1):
            name = helpers.colorme(f"{line_num} - {organization['name']}", "green")
            print(f"    {name}")
        selected = helpers.validate_integer_in_range(len(organizations))
        return (
            organizations[int(selected)]["id"],
            organizations[int(selected)]["name"],
        )

    def select_network(self, org, lines_to_display=25):
        """Lists the organization networks and prompts user to select one

        Args:
            dashboard (obj): The Meraki dashboard instance
            org (str): The selected organization ID
            lines_to_display (int): The number of lines before pausing

        Returns:
            list: the selected network ID and network name
        """

        network_list = []
        try:
            logger.debug("Trying to get networks from the Meraki dashboard")
            networks = self.dashboard.organizations.getOrganizationNetworks(org)
            while not network_list:
                search_name = input(
                    "Enter a name to search for or leave blank for all networks: "
                )
                if search_name:
                    for network in networks:
                        if search_name.lower() in network["name"].lower():
                            network_list.append(network)
                else:
                    network_list = networks
                if network_list:
                    network_list.sort(key=lambda x: x["name"])
                    print("\nNetworks:")
                    for line_num, net in enumerate(network_list, start=1):
                        net_name = net["name"]
                        print(f"{line_num} - {net_name}")
                        if line_num % lines_to_display == 0:
                            user_response = input(
                                "\nPress Enter to continue, or q + Enter to quit search: "
                            )
                            if "q" in user_response:
                                break
                else:
                    print(f"No networks found matching {search_name}")

            selected = helpers.validate_integer_in_range(len(network_list))
            return [
                network_list[int(selected)]["id"],
                network_list[int(selected)]["name"],
            ]

        except Exception as err:
            logger.debug(
                f"Error while trying to get organization networks for org ID {org}"
            )
            logger.debug(err.args)
            print(
                helpers.colorme(
                    "Error retieving networks, verify org ID is set properly", "red"
                )
            )
            return ("", "")

    def get_group_policies(self, netid):
        logger.debug(
            f'The "get_group_policies" function called with network ID {netid}'
        )
        group_policies = []
        group_policies = self.dashboard.networks.getNetworkGroupPolicies(netid)
        if not group_policies:
            logger.info(f"No group policies found for network ID {netid}")
            net_id = helpers.colorme(netid, "blue")
            print(f"  No group policies found for network ID {net_id}")
        for gp in group_policies:
            logger.info(f"Found group policy with name \"{gp['name']}\"")
            gp_name = helpers.colorme(gp["name"], "blue")
            print(f"  Found Policy Name: {gp_name}")

    def view_group_policy(self, netid):
        logger.debug(f'The "view_group_policy" function called with net_id {netid}')
        policy_name = input("Please enter the name of the group policy to view: ")
        group_policies = self.dashboard.networks.getNetworkGroupPolicies(netid)
        for gp in group_policies:
            if policy_name == gp["name"]:
                print(json.dumps(gp, indent=2))
                return True
        logger.info(f'The specified group policy "{policy_name}" was not found')
        return False

    def create_group_policy(self):
        logger.debug('The "create_group_policy" function called')
        group_policy = []
        policy_name = policy_source = destinations = ""
        # Load the values needed to complete this operation or exit
        if helpers.get_settings.get_value("group_policies.source_policy_name"):
            policy_name = helpers.get_settings.get_value(
                "group_policies.source_policy_name"
            )
        if helpers.get_settings.get_value("group_policies.source_network_id"):
            policy_source = helpers.get_settings.get_value(
                "group_policies.source_network_id"
            )
        if helpers.get_settings.get_value("group_policies.destinations_file"):
            destinations = helpers.get_settings.get_value(
                "group_policies.destinations_file"
            )
        if not policy_name or not policy_source or not destinations:
            logger.info("Missing some values that are needed for create operation")
            logger.info("Please confirm group_policies section in settings.toml file")
            print(helpers.colorme("Error: Missing values needed for operation", "red"))
            sys.exit("Please fill out the group_policies section in the settings file")
        # Pull source policy from specified source network
        group_policies = self.dashboard.networks.getNetworkGroupPolicies(policy_source)
        for policy in group_policies:
            if policy_name == policy["name"]:
                group_policy = policy
        if not group_policy:
            logger.info(f"Specified source policy name {policy_name} was not found.")
            logger.info("Please ensure that the source policy name is correct")
            print(helpers.colorme("Error: Cannot continue", "red"))
            sys.exit("Please ensure that the source policy name is correct")
        # Load the destination networks from the specified file
        networks = helpers.get_networks_list(destinations)
        # Prepare the progress bar
        progress = 0
        total = len(networks)
        # Everything is ready to go. Write the group policy to each requested network
        for network in networks:
            bar = helpers.progress_bar(progress, total)
            print(bar, end="", flush=True)
            network_id = network.split(",")[0]
            network_name = network.split(",")[1]
            if not (network_id.startswith("L_") or network_id.startswith("N_")):
                logger.info("Check the destination input file for errors")
                logger.info(f"The network ID {network_id} is incorrect")
                print(helpers.colorme("Error: Cannot continue", "red"))
                sys.exit("Found an invalid network ID, check destinations file")
            try:
                logger.debug(f"Creating group policy for network {network_name}")
                self.dashboard.networks.createNetworkGroupPolicy(
                    network_id,
                    policy_name,
                    scheduling=group_policy["scheduling"],
                    bandwidth=group_policy["bandwidth"],
                    firewallAndTrafficShaping=group_policy["firewallAndTrafficShaping"],
                    contentFiltering=group_policy["contentFiltering"],
                    # Wireless only settings for the next three
                    splashAuthSettings=group_policy["splashAuthSettings"],
                    vlanTagging=group_policy["vlanTagging"],
                    bonjourForwarding=group_policy["bonjourForwarding"],
                )
                logger.info(
                    f"Group policy {policy_name} created for network {network_name}"
                )
            except Exception as api_error:
                logger.info(f"Failed to write group policy for {network_name}")
                logger.info(api_error)
            progress += 1
            print("\b" * len(bar), end="", flush=True)
        bar = helpers.progress_bar(progress, total)
        print(bar, end="", flush=True)
        print("\n")

    def delete_group_policy(self, netid):
        logger.debug(f'The "delete_group_policy" function called with net_id {netid}')
        policy_name = input("Please enter the name of the group policy to delete: ")
        group_policies = self.dashboard.networks.getNetworkGroupPolicies(netid)
        for gp in group_policies:
            if policy_name == gp["name"]:
                self.dashboard.networks.deleteNetworkGroupPolicy(
                    netid, gp["groupPolicyId"]
                )
                logger.info(
                    f"Successfully deleted group policy with name {policy_name}"
                )
                return True
        logger.info(f"Failed to delete group policy with name {policy_name}")
        logger.info("Please confirm that the name is correct and try again.")
        return False

    def get_wireless_networks(self, organization_id):
        logger.debug(
            f'The "get_wireless_networks" function called with org_id {organization_id}'
        )
        networks = self.dashboard.organizations.getOrganizationNetworks(
            organization_id, total_pages="all"
        )
        total = 0
        wireless = 0
        no_wireless = 0
        wireless_networks = []
        for network in networks:
            if "wireless" in network["productTypes"]:
                wireless_networks.append(network["id"] + "," + network["name"] + "\n")
                logger.info(
                    f'network {network["name"]}, \
                    was identified as having some type of wireless'
                )
                wireless += 1
                total += 1
            else:
                logger.info(
                    f"network {network['name']}, \
                    was identified as not having some type of wireless"
                )
                no_wireless += 1
        logger.info(
            f"INFO: There are {wireless} sites with some type of wireless device"
        )
        logger.info(f"INFO: There were {no_wireless} sites with no wireless")
        return wireless_networks

    def find_ssid_number(self):
        logger.debug('The "wheres_ssid" function called')
        search_ssid = helpers.get_settings.get_value("networks_with_ssid.ssid")
        input_file = helpers.get_settings.get_value("networks_with_ssid.input_file")
        networks = helpers.get_networks_list(input_file)
        path = helpers.get_settings.get_value("networks_with_ssid.output_file")
        logger.debug(f'Searching for ssid "{search_ssid}"')
        logger.debug(f'Searching for networks found in "{input_file}"')
        logger.debug(f'Writting to path "{path}"')
        progress = found_count = not_found_count = 0
        total = len(networks)
        logger.info(f"The total number of networks is {total}")
        ssid_sites = []
        print()
        for network in networks:
            bar = helpers.progress_bar(progress, total)
            print(bar, end="", flush=True)
            site = network.split(",")
            site_id = site[0]
            site_name = site[1]
            logger.debug(
                f"Calling Meraki dashboard to pull all SSIDs for network {site_id}"
            )
            ssids = self.dashboard.wireless.getNetworkWirelessSsids(site_id)
            found_ssid = False
            for ssid in ssids:
                if ssid["name"] == search_ssid:
                    found_ssid = True
                    newline = f'{site_id},{site_name},{ssid["name"]},\
                    {ssid["number"]},{ssid["enabled"]}\n'
                    ssid_sites.append(newline)
                    logger.info(f'Found SSID {search_ssid} for "{site_name}"')
                    found_count += 1
                    progress += 1
            if not found_ssid:
                logger.info(f'SSID {search_ssid} was not found for "{site_name}"')
                not_found_count += 1
                progress += 1
            print("\b" * len(bar), end="", flush=True)
        bar = helpers.progress_bar(progress, total)
        print(bar, end="", flush=True)
        print("\n")
        helpers.writelines_to_file(path, ssid_sites)
        logger.info(f"Sites with SSID {search_ssid}, found {found_count}")
        logger.info(f"Sites without SSID {search_ssid}, found {not_found_count}")

    def update_radius_servers(self):
        logger.debug('The "update_radius_servers" function called')
        input_file = helpers.get_settings.get_value("radius.input_file")
        networks = helpers.get_networks_list(input_file)
        radius, accounting = helpers.format_radius()
        logger.debug(f'Searching for networks "{networks}"')
        logger.debug(f'Searching for radius servers "{radius}"')
        logger.debug(f'Searching for accounting servers "{accounting}"')
        progress = 0
        total = len(networks)
        for network in networks:
            bar = helpers.progress_bar(progress, total)
            print(bar, end="", flush=True)
            site = network.split(",")
            net_id = site[0]
            net_name = site[1]
            ssid_num = site[3]
            logger.info(
                f"Updating radius settings for {net_name} and SSID number {ssid_num}"
            )
            logger.debug(
                f"Calling Meraki dashboard with"
                f"{net_id} {ssid_num} {radius} {accounting}"
            )
            try:
                self.dashboard.wireless.updateNetworkWirelessSsid(
                    networkId=net_id,
                    number=ssid_num,
                    radiusServers=radius,
                    radiusAccountingServers=accounting,
                )
            except Exception as api_error:
                logger.info(f"Failed to update SSID for {net_name}")
                logger.debug(api_error)
            progress += 1
            print("\b" * len(bar), end="", flush=True)
        logger.info(f"Updated radius settings on {progress} SSIDs")
        bar = helpers.progress_bar(progress, total)
        print(bar, end="", flush=True)
        print("\n")

    def enable_disable_paticular_ssid(self, ssid_enabled):
        logger.debug('The "enable_disable_paticular_ssid" function called')
        status = "enabled" if ssid_enabled else "disabled"
        input_file = helpers.get_settings.get_value("ssid_enabled_status.input_file")
        networks = helpers.get_networks_list(input_file)
        progress = 0
        total = len(networks)
        print()
        for network in networks:
            bar = helpers.progress_bar(progress, total)
            print(bar, end="", flush=True)
            site = network.split(",")
            site_id = site[0]
            site_name = site[1]
            ssid_name = site[2]
            ssid_num = site[3]
            logger.info(f"Changing status for {site_name} ssid {ssid_name} to {status}")
            try:
                self.dashboard.wireless.updateNetworkWirelessSsid(
                    networkId=site_id, number=ssid_num, enabled=ssid_enabled
                )
            except Exception as api_error:
                logger.info(f"Failed to update SSID for {site_name}")
                logger.debug(api_error)
            progress += 1
            print("\b" * len(bar), end="", flush=True)
        bar = helpers.progress_bar(progress, total)
        print(bar, end="", flush=True)
        print("\n")
