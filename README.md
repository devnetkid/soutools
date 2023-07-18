# SoUTools

## Overview

This simple cli menu tool allows you to select an organization from the Meraki dashboard. With an organization selected
you can then go to the wireless options and pull down a list of all the networks that have a product type of wireless.
From that list you can generate a report that searches all the wireless sites for a particular SSID. Now that you have 
that information you can then modify something about those particular networks. The third option of this program specifically
updates the radius settings but you could easily modify that to change any of the other settings related to an SSID.

## Setup

1. You must enable API access in the Meraki Dashboard if you haven't already.
2. It is recommended that you store your API key in an environment variable.
   However, if you prefer you can also add it to the settings_template.toml file.
3. Also, in the settings_template.toml file you will at a minimum, need to update
   the radius settings with your radius information.
4. The final step would be to change the settings_template.toml to settings.toml

**Adding the environment varialbe**

The default environment variable is "MERAKI_DASHBOARD_API_KEY". If you want to change
this then you can update the "API_KEY_ENVIRONMENT_VARIABLE" under the MERAKI settings
of the settings_template.toml file.

**Some specifics**

On linux

    export MERAKI_DASHBOARD_API_KEY=123abc456def789

On Windows

1. Press the windows key or click on windows icon in the lower left hand corner of screen
2. Type env and press enter. This should pop open the window titled System Properties
3. Under the Advanced tab click Environment Variables... button
4. Under the first section titled User varialbes for username, click on New... button.
5. Enter in the Variable Name: MERAKI_DASHBOARD_API_KEY
6. Enter in the Variable value: 123abc456def789
7. Press OK on each of the open windows to save changes.
8. If you had the command prompt open you will need to close and re-open for changes to take effect.

## Usage

To use the program, open a terminal window and type `soutools`
You will see a menu with four options

    1 - Select an organization
    2 - View the selected organization
    3 - Wireless options
    4 - Exit

If you haven't entered a DEFAULT_ORG_ID in the settings.toml file then you will need to start with 1.
You can use 2 to confirm which organization ID is selected.
Once you have your organization ID go to 3 wireless options. You will see something similar to the following:

    1 - Generate a report of all sites of type wireless
    2 - Generate a report of all sites with a particular SSID
    3 - Update radius servers for a particular SSID
    4 - Return to previous menu
    5 - Exit

Start with 1 to build a report of sites that do have wireless. A file will be written to what you have specified
under section 3.1 output_file. The file will include network_id,network_name. See following ficticous data:

    2394582934587239847,mysite1
    4239458293458729847,mysite2
    2739458293458729847,mysite3
    1394582934587239847,mysite4
    ...

Once you have that list move onto option 2 to find the sites that have the SSID you require to be changed.

    2394582934587239847,mysite1,mySSID,0
    4239458293458729847,mysite2,mySSID,0
    2739458293458729847,mysite3,mySSID,1
    1394582934587239847,mysite4,mySSID,0
    ...

The final step in the process, option 3, is the step that will take the data you have built up from the previous steps
and use it to change the radius settings of the given SSID. Check the output logs specified in the settings file to see 
the final results

    # Overall settings
    [LOGGING]
    log_level = 'info'
    log_path = 'output/logs/logs.log'


