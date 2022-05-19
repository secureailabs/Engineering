# -----------------------------------------------------------
#
# Class DataSetManagementApi
#
# -----------------------------------------------------------
import requests
from utils.helpers import get_response_values


class DataSetManagementApi:
    """
    DataSets Api Class
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def list_datasets(self, sail_portal):
        """
        List Datasets

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb}
        # Attempt to list applicable dataset for logined user
        try:
            #  params as json
            response = requests.get(f"{self.base_url}/SAIL/DatasetManager/ListDatasets", json=json_params, verify=False)
            # params query string
            # response = requests.get(
            #     f"{self.base_url}/SAIL/DatasetManager/ListDatasets", params=query_params, verify=False
            # )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def pull_dataset(self, sail_portal, dataset_guid):
        """
        Pull Dataset

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb, "DatasetGuid": dataset_guid}
        # Attempt to pull applicable dataset information
        try:
            #  params as json
            response = requests.get(f"{self.base_url}/SAIL/DatasetManager/PullDataset", json=json_params, verify=False)
            # params query string
            # response = requests.get(
            #     f"{self.base_url}/SAIL/DatasetManager/PullDataset", params=query_params, verify=False
            # )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def register_dataset(self, sail_portal, payload):
        """
        Add Register a new dataset

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
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
                f"{self.base_url}/SAIL/DatasetManager/RegisterDataset",
                json=json_params,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def delete_dataset(self, sail_portal, payload):
        """
        Delete registered dataset

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        json_params = {"Eosb": user_eosb}
        json_params.update(payload)
        # query_params = url_encoded(json_params)
        try:
            # params as json
            # returns a 404 BOARD-314
            response = requests.delete(
                f"{self.base_url}/SAIL/DatasetManager/DeleteDataset",
                json=json_params,
                verify=False,
            )

            # params query string
            # response = requests.delete(
            #     f"{self.base_url}/SAIL/DatasetManager/DeleteDataset", params=query_params, verify=False
            # )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)
