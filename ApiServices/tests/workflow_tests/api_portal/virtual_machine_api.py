# -------------------------------------------------------------------------------
# Engineering
# virtual_machine_api.py
# -------------------------------------------------------------------------------
"""Virtual Machine Api Module"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
import requests
from tests.workflow_tests.utils.helpers import get_response_values


class VirtualMachineApi:
    """
    Virtual Machine Management Api Class
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def list_virtual_machines(self, sail_portal):
        """
        List Virtual Machines associated to user

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        json_params = {"Eosb": user_eosb}

        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/SAIL/VirtualMachineManager/ListVirtualMachines", json=json_params, verify=False
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def virtual_machines_status(self, sail_portal, payload):
        """
        Get Virtual Machine's Full Status

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        json_params = {"Eosb": user_eosb}
        json_params.update(payload)

        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/SAIL/VirtualMachineManager/PullVirtualMachine", json=json_params, verify=False
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)
