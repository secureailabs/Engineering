# -------------------------------------------------------------------------------
# Engineering
# dataset_management_api.py
# -------------------------------------------------------------------------------
"""Data Set Management Api Module"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
import requests
from tests.workflow_tests.api_portal.sail_portal_api import SailPortalFastApi
from tests.workflow_tests.utils.dataset_helpers import Dataset, DatasetVersion
from tests.workflow_tests.utils.helpers import get_response_values


class DataSetManagementFastApi:
    """
    DataSets FastApi Class
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_all_datasets(self, sail_portal: SailPortalFastApi):
        """
        Get all datasets.\n
        [GET] /datasets

        :param sail_portal: fixture, SailPortalFastApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalFastApi
        :returns: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        try:
            response = requests.get(
                f"{self.base_url}/datasets", headers=request_headers, verify=False
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code
        return response, response.json()

    def register_dataset(self, sail_portal: SailPortalFastApi, payload: Dataset):
        """
        Add Register a new dataset.\n
        [POST] /datasets

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        json_params = {
            "name": payload.name,
            "description": payload.description,
            "tags": payload.tags,
            "format": payload.format,
        }

        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/datasets",
                verify=False,
                headers=request_headers,
                json=json_params,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response, response.json()

    def get_dataset_by_id(self, sail_portal: SailPortalFastApi, dataset_id: str):
        """
        Get dataset by ID.\n
        [GET] /datasets/{dataset_id}

        :param sail_portal: fixture, SailPortalFastApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalFastApi
        :param dataset_id: dataset ID
        :type dataset_id: string
        :returns: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        try:
            response = requests.get(
                f"{self.base_url}/datasets/{dataset_id}",
                headers=request_headers,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code
        return response, response.json()

    def update_dataset(
        self, sail_portal: SailPortalFastApi, dataset_id: str, payload: Dataset
    ):
        """
        Update dataset.\n
        [PUT] /datasets/{dataset_id}

        :param sail_portal: fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param dataset_id: dataset ID
        :type dataset_id: string
        :param payload: payload of new data
        :type payload: Dataset
        :return: response
        :rtype: string
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        json_params = {
            "name": payload.name,
            "description": payload.description,
            "tags": payload.tags,
        }

        # Attempt to update organization info
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/datasets/{dataset_id}",
                verify=False,
                headers=request_headers,
                json=json_params,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response

    def delete_dataset_by_id(self, sail_portal: SailPortalFastApi, dataset_id: str):
        """
        Delete a dataset.\n
        [DELETE] /datasets/{dataset_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param dataset_id: dataset ID
        :type dataset_id: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to delete an organization
        try:
            #  params as json
            response = requests.delete(
                f"{self.base_url}/datasets/{dataset_id}",
                verify=False,
                headers=request_headers,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response

    def get_all_dataset_versions(self, sail_portal: SailPortalFastApi, dataset_id: str):
        """
        Get all dataset versions.\n
        [GET] /dataset-versions

        :param sail_portal: fixture, SailPortalFastApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalFastApi
        :returns: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}
        json_params = {"dataset_id": dataset_id}

        try:
            response = requests.get(
                f"{self.base_url}/dataset-versions?dataset_id={dataset_id}",
                headers=request_headers,
                json=json_params,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code
        return response, response.json()

    def register_dataset_version(
        self, sail_portal: SailPortalFastApi, payload: DatasetVersion
    ):
        """
        Add Register a new dataset version.\n
        [POST] /dataset-versions

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: DatasetVersion
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        json_params = {
            "dataset_id": payload.dataset_id,
            "description": payload.description,
            "name": payload.name,
        }

        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/dataset-versions",
                verify=False,
                headers=request_headers,
                json=json_params,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output
        return response, response.json()

    def get_dataset_version_by_id(
        self, sail_portal: SailPortalFastApi, dataset_version_id: str
    ):
        """
        Get dataset-version by ID.\n
        [GET] /dataset-version/{dataset_version_id}

        :param sail_portal: fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param dataset_id: dataset-version ID
        :type dataset_id: string
        :returns: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        try:
            response = requests.get(
                f"{self.base_url}/dataset-versions/{dataset_version_id}",
                headers=request_headers,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response, response.json()

    def update_dataset_version(
        self,
        sail_portal: SailPortalFastApi,
        dataset_version_id: str,
        payload: DatasetVersion,
    ):
        """
        Update dataset-version.\n
        [PUT] /dataset-versions/{dataset_version_id}

        :param sail_portal: fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param dataset_id: dataset-version ID
        :type dataset_id: string
        :param payload: payload of new data
        :type payload: DatasetVersion
        :return: response
        :rtype: string
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        json_params = {
            "description": payload.description,
            "state": payload.state,
        }

        # Attempt to update organization info
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/dataset-versions/{dataset_version_id}",
                verify=False,
                headers=request_headers,
                json=json_params,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response

    def delete_dataset_version_by_id(
        self, sail_portal: SailPortalFastApi, dataset_version_id: str
    ):
        """
        Delete a dataset-version.\n
        [DELETE] /dataset-versions/{dataset_version_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param dataset_version_id: dataset-version ID
        :type dataset_version_id: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to delete an organization
        try:
            #  params as json
            response = requests.delete(
                f"{self.base_url}/dataset-versions/{dataset_version_id}",
                verify=False,
                headers=request_headers,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response


class DataSetManagementApi:
    """
    DataSets Api Class
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

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
            response = requests.get(
                f"{self.base_url}/SAIL/DatasetManager/ListDatasets",
                json=json_params,
                verify=False,
            )
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
            response = requests.get(
                f"{self.base_url}/SAIL/DatasetManager/PullDataset",
                json=json_params,
                verify=False,
            )
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
