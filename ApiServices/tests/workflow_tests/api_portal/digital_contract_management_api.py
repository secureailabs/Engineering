# -----------------------------------------------------------
#
# Class DigitalContractManagementApi
#
# -----------------------------------------------------------
import requests

# from utils.helpers import url_encoded
from tests.workflow_tests.utils.helpers import get_response_values


class DigitalContractManagementApi:
    """
    Digital Contract Management Api Class
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def list_digital_contracts(self, sail_portal):
        """
        List Digital Contract Information

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        sail_portal.get_basic_user_info()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb}
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/SAIL/DigitalContractManager/DigitalContracts", json=json_params, verify=False
            )
            # params query string
            # response = requests.gn
            # et(
            #     f"{self.base_url}/SAIL/DatasetManager/ListDatasets", params=query_params, verify=False
            # )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def pull_digital_contract(self, sail_portal, digital_contract_guid):
        """
        Pull Digital Contract information

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param digital_contract_guid: digital contract guid
        :type digital_contract_guid: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb, "DigitalContractGuid": digital_contract_guid}
        # Attempt to pull applicable dataset information
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/SAIL/DigitalContractManager/PullDigitalContract", json=json_params, verify=False
            )
            # params query string
            # response = requests.get(
            #     f"{self.base_url}/SAIL/DatasetManager/PullDataset", params=query_params, verify=False
            # )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def register_digital_contract(self, sail_portal, payload):
        """
        Register Digital Contract

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb}
        json_params.update(payload)

        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/SAIL/DigitalContractManager/Applications",
                json=json_params,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def accept_digital_contract(self, sail_portal, payload):
        """
        Accept Digital Contract

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb}
        json_params.update(payload)

        try:
            #  params as json
            response = requests.patch(
                f"{self.base_url}/SAIL/DigitalContractManager/DataOwner/Accept",
                json=json_params,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def activate_digital_contract(self, sail_portal, payload):
        """
        Activate Digital Contract

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb}
        json_params.update(payload)
        try:
            #  params as json
            response = requests.patch(
                f"{self.base_url}/SAIL/DigitalContractManager/Researcher/Activate",
                json=json_params,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def associate_digital_contract(self, sail_portal, payload):
        """
        Associate Digital Contract

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb}
        json_params.update(payload)
        try:
            #  params as json
            response = requests.patch(
                f"{self.base_url}/SAIL/DigitalContractManager/AssociateWithAzureTemplate",
                json=json_params,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def provision_digital_contract(self, sail_portal, payload):
        """
        provision Digital Contract

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb}
        json_params.update(payload)
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/SAIL/DigitalContractManager/Provision",
                json=json_params,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def get_provision_dc_status(self, sail_portal, payload):
        """
        get provision Digital Contract status

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb}
        json_params.update(payload)
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/SAIL/DigitalContractManager/GetProvisioningStatus",
                json=json_params,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def deprovision_digital_contract(self, sail_portal, payload):
        """
        Deprovision Digital Contract

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb}
        json_params.update(payload)
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/SAIL/DigitalContractManager/Deprovision",
                json=json_params,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)
