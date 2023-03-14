# -------------------------------------------------------------------------------
# Engineering
# azure_template_managment_api.py
# -------------------------------------------------------------------------------
"""Azure Template Api Module"""
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


class AzureTemplateApi:
    """
    Azure Template Api Class
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def list_azure_templates(self, sail_portal):
        """
        List Azure Template

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb}
        try:
            #  params as json
            response = requests.get(f"{self.base_url}/SAIL/AzureManager/ListTemplates", json=json_params, verify=False)
            # params query string
            # response = requests.gn
            # et(
            #     f"{self.base_url}/SAIL/DatasetManager/ListDatasets", params=query_params, verify=False
            # )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def pull_azure_template(self, sail_portal, payload):
        """
        Pull Azure Template

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param template_guid: template guid
        :type template_guid: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb, "TemplateGuid": template_guid})
        json_params = {"Eosb": user_eosb, "TemplateGuid": payload}
        try:
            #  params as json
            response = requests.get(f"{self.base_url}/SAIL/AzureManager/PullTemplate", json=json_params, verify=False)
            # params query string
            # response = requests.gn
            # et(
            #     f"{self.base_url}/SAIL/AzureManager/PullTemplate", params=query_params, verify=False
            # )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def register_azure_template(self, sail_portal, payload):
        """
        Add Register a new Azure Template

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: template payload
        :type payload: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        json_params = {"Eosb": user_eosb}
        json_params.update(payload)
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/SAIL/AzureManager/RegisterTemplate",
                json=json_params,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def update_azure_template(self, sail_portal, payload):
        """
        Update information in Azure Template

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: template payload
        :type payload: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        json_params = {"Eosb": user_eosb}
        json_params.update(payload)
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/SAIL/AzureManager/UpdateTemplate",
                json=json_params,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def delete_azure_template(self, sail_portal, payload):
        """
        Delete information in Azure Template

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: template payload
        :type payload: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        json_params = {"Eosb": user_eosb}
        json_params.update(payload)
        try:
            #  params as json
            response = requests.delete(
                f"{self.base_url}/SAIL/AzureManager/DeleteTemplate",
                json=json_params,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)
