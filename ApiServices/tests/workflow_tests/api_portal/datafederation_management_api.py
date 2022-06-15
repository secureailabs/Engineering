# -----------------------------------------------------------
#
# Class DataFederationManagementApi
#
# -----------------------------------------------------------
import requests
from tests.workflow_tests.utils.helpers import get_response_values


class DataFederationManagementApi:
    """
    Data Federation Management Api Class
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def list_data_federations(self, sail_portal):
        _, _, user_eosb = sail_portal.login()
        payload = {}
        payload["Eosb"] = user_eosb

        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/SAIL/DataFederationManager/ListDataFederations",
                json=payload,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response
        return get_response_values(response)

    def register_data_federation(self, sail_portal, payload):
        """
        Register Data federation

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

        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/SAIL/DataFederationManager/RegisterDataFederation",
                json=payload,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response
        return get_response_values(response)

    def delete_data_federation(self, sail_portal, dataset_family_guid):
        return ""

    def update_data_federation(self, sail_portal, dataset_family):
        return ""
