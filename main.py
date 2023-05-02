"""
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import meraki
import config
import requests
import json

base_url = "https://api.meraki.com/api/v1"
dashboard = meraki.DashboardAPI(api_key=config.api_key,print_console=False)

orgs = dashboard.organizations.getOrganizations()
for org in orgs:
    if config.org_name in org["name"]:
        networks = dashboard.organizations.getOrganizationNetworks(organizationId=org["id"])
        for network in networks:
            network_id = network["id"]
            devices = dashboard.networks.getNetworkDevices(networkId=network["id"])
            for device in devices:
                device_serial = device["serial"]
                if device["model"].startswith("MS"):
                    print(device)
                    if device["serial"] in config.device_list:
                        print(device)
                    else:
                        continue
                    # Get device management interface settings
                    url = f"{base_url}/devices/{device_serial}/managementInterface"
                    headers = {"X-Cisco-Meraki-API-Key": config.api_key}
                    response = requests.get(url, headers=headers)

                    # Update device management interface settings with new static DNS
                    if response.status_code == 200:
                        current_settings = json.loads(response.content)
                        current_settings["wan1"]["staticDns"] = config.new_static_dns
                        url = f"{base_url}/devices/{device_serial}/managementInterface"
                        response = requests.put(url, headers=headers, json=current_settings)
                        if response.status_code == 200:
                            print("Device management interface updated successfully.")
                        else:
                            print("Failed to update device management interface.")
                    else:
                        print("Failed to get device management interface settings.")
                    print(response)
    else:
        continue