# -------------------------------------------------------------------------------
# Engineering
# dataset_management_api.py
# -------------------------------------------------------------------------------
"""Dataset Family Management Api Module"""
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


class DatasetFamilyManagementApi:
    """
    Dataset Family Management Api Class
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def list_dataset_families(self, sail_portal):
        """
        List Dataset Family Information

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
                f"{self.base_url}/SAIL/DatasetFamilyManager/ListDatasetFamilies", json=json_params, verify=False
            )

        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def pull_dataset_family(self, sail_portal, dataset_family_guid):
        """
        Pull Dataset Family information

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param dataset_family_guid: dataset family guid
        :type dataset_family_guid: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb, "DatasetFamilyGuid": dataset_family_guid}
        # Attempt to pull applicable dataset information
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/SAIL/DatasetFamilyManager/PullDatasetFamily", json=json_params, verify=False
            )

        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def register_dataset_family(self, sail_portal, payload):
        """
        Register Dataset Family

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: string
        :return: response
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()

        # Attach the logged in user's EOSB
        payload["Eosb"] = user_eosb
        print(payload)
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/SAIL/DatasetFamilyManager/RegisterDatasetFamily",
                json=payload,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response
        return get_response_values(response)

    def delete_dataset_family(self, sail_portal, dataset_family_guid):
        """
        Delete Dataset Family information

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param dataset_family_guid: dataset family guid
        :type dataset_family_guid: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb, "DatasetFamilyGuid": dataset_family_guid}
        # Attempt to pull applicable dataset information
        try:
            #  params as json
            response = requests.delete(
                f"{self.base_url}/SAIL/DatasetFamilyManager/DeleteDatasetFamily", json=json_params, verify=False
            )

        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def update_datset_family(self, sail_portal, dataset_family):
        """
        Delete Dataset Family information

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param dataset_family_guid: dataset family guid
        :type dataset_family_guid: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb, "DatasetFamily": dataset_family}
        # Attempt to pull applicable dataset information
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/SAIL/DatasetFamilyManager/UpdateDatasetFamily", json=json_params, verify=False
            )

        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)
