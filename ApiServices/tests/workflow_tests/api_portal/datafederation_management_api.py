# -------------------------------------------------------------------------------
# Engineering
# datafederation_management_api.py
# -------------------------------------------------------------------------------
"""Data Federation Management Api Module"""
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
from tests.workflow_tests.utils.federation_helpers import DataFederation
from tests.workflow_tests.utils.helpers import get_response_values


class DataFederationManagementFastApi:
    """
    Data Federation Management Fast Api Class
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_all_data_federations(self, sail_portal: SailPortalFastApi):
        """
        Get all data federations associated with a dataset.\n
        [GET] /data-federations

        :param data_owner_portal: data owner sail portal
        :type data_owner_portal: SailPortalFastApi
        :param researcher_portal: researcher sail portal
        :type researcher_portal: SailPortalFastApi
        :param dataset_id: dataset ID
        :type dataset_id: str
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )

        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        try:
            response = requests.get(
                f"{self.base_url}/data-federations",
                headers=request_headers,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code
        return response, response.json()

    def register_data_federation(
        self, sail_portal: SailPortalFastApi, new_federation: DataFederation
    ):
        """
        Register a new data federation.\n
        [POST] /data-federations

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param name: name of federation
        :type name: str
        :param description: description of federation
        :type description: str
        :param data_format: data format of federation
        :type data_format: str
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        json_params = {
            "name": new_federation.name,
            "description": new_federation.description,
            "data_format": new_federation.format,
        }

        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/data-federations",
                verify=False,
                headers=request_headers,
                json=json_params,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output
        return response, response.json()

    def get_data_federation_by_id(
        self, sail_portal: SailPortalFastApi, federation_id: str
    ):
        """
        Get a data federation by ID.\n
        [GET] /data-federations/{data_federation_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param federation_id: target federation ID
        :type federation_id: str
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        try:
            response = requests.get(
                f"{self.base_url}/data-federations/{federation_id}",
                headers=request_headers,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code
        return response, response.json()

    def update_data_federation(
        self, sail_portal: SailPortalFastApi, federation_id: str, payload
    ):
        """
        Update an existing data federation.\n
        [PUT] /data-federations/{data_federation_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param federation_id: ID of federation to be updated
        :type federation_id: str
        :param new_name: new name of federation
        :type new_name: str
        :param new_description: new description of federation
        :type new_description: str
        :return: response
        :rtype: string
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        json_params = payload

        # Attempt to update data federation info
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/data-federations/{federation_id}",
                verify=False,
                headers=request_headers,
                json=json_params,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response

    def delete_data_federation_by_id(
        self, sail_portal: SailPortalFastApi, federation_id: str
    ):
        """
        Soft delete a data federation.\n
        [DELETE] /data-federations/{data_federation_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param federation_id: ID of federation to be deleted
        :type federation_id: str
        :return: response
        :rtype: string
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to delete an organization
        try:
            #  params as json
            response = requests.delete(
                f"{self.base_url}/data-federations/{federation_id}",
                verify=False,
                headers=request_headers,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response

    def invite_researcher_to_data_federation(
        self, sail_portal: SailPortalFastApi, federation_id: str, researcher_org_id: str
    ):
        """
        Invite a researcher to join the data federation.\n
        [PUT] /data-federations/{data_federation_id}/researcher/{researcher_organization_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param federation_id: federation ID
        :type federation_id: str
        :param researcher_org_id: researcher organization ID
        :type researcher_org_id: str
        :return: response
        :rtype: string
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to update data federation info
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/data-federations/{federation_id}/researcher/{researcher_org_id}",
                verify=False,
                headers=request_headers,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response

    def register_researcher_to_data_federation(
        self, sail_portal: SailPortalFastApi, federation_id: str, researcher_org_id: str
    ):
        """
        Automatically register a researcher to the data federation, bypassing an invite path.\n
        [POST] /data-federations/{data_federation_id}/researcher/{researcher_organization_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param federation_id: federation ID
        :type federation_id: str
        :param researcher_org_id: researcher organization ID
        :type researcher_org_id: str
        :return: response
        :rtype: string
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to update data federation info
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/data-federations/{federation_id}/researcher/{researcher_org_id}",
                verify=False,
                headers=request_headers,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response

    def invite_data_submitter_to_data_federation(
        self, sail_portal: SailPortalFastApi, federation_id: str, submitter_org_id: str
    ):
        """
        Invite a data submitter to join the data federation.\n
        [PUT] /data-federations/{data_federation_id}/data-submitter/{data_submitter_organization_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param federation_id: federation ID
        :type federation_id: str
        :param submitter_org_id: data submitter organization ID
        :type submitter_org_id: str
        :return: response
        :rtype: string
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to update data federation info
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/data-federations/{federation_id}/data-submitter/{submitter_org_id}",
                verify=False,
                headers=request_headers,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response

    def register_data_submitter_to_data_federation(
        self, sail_portal: SailPortalFastApi, federation_id: str, submitter_org_id: str
    ):
        """
        Automatically register a data submitter to the data federation, bypassing an invite path.\n
        [POST] /data-federations/{data_federation_id}/data-submitter/{data_submitter_organization_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param federation_id: federation ID
        :type federation_id: str
        :param submitter_org_id: data submitter organization ID
        :type submitter_org_id: str
        :return: response
        :rtype: string
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to update data federation info
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/data-federations/{federation_id}/data-submitter/{submitter_org_id}",
                verify=False,
                headers=request_headers,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response

    # TODO: Currently throws [500] Internal Server Error when trying to get all invites
    def get_all_data_federation_organization_invites(
        self, sail_portal: SailPortalFastApi, organization_id: str
    ):
        """
        Get a list of all pending federation invites for an organization. Only ADMIN roles have access.\n
        [GET] /data-federations/{organization_id}/invites

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param organization_id: organization ID
        :type organization_id: str
        :return: response
        :rtype: string
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        try:
            response = requests.get(
                f"{self.base_url}/data-federations/{organization_id}/invites",
                headers=request_headers,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code
        return response

    def get_data_federation_organization_invite_by_id(
        self, sail_portal: SailPortalFastApi, organization_id: str, invite_id: str
    ):
        """
        Get information about an invite.\n
        [GET] /data-federations/{organization_id}/invites/{invite_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param organization_id: organization ID
        :type organization_id: str
        :param invite_id: invite ID
        :type invite_id: str
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        try:
            response = requests.get(
                f"{self.base_url}/data-federations/{organization_id}/invites/{invite_id}",
                headers=request_headers,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code
        return response, response.json()

    def accept_or_reject_data_federation_invite(
        self,
        sail_portal: SailPortalFastApi,
        org_id: str,
        invite_id: str,
        invite_state: str,
    ):
        """
        Accept or reject a data federation invite for an organization.\n
        [PATCH] /data-federations/{organization_id}/invites/{invite_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param org_id: organization ID
        :type org_id: str
        :param invite_id: invite ID
        :type invite_id: str
        :param invite_state: status of invite
        :type invite_state: str
        :return: response
        :rtype: string
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        json_params = {
            "state": invite_state,
        }

        # Attempt to update data federation info
        try:
            #  params as json
            response = requests.patch(
                f"{self.base_url}/data-federations/{org_id}/invites/{invite_id}",
                verify=False,
                headers=request_headers,
                json=json_params,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response

    def add_dataset_to_federation(
        self, sail_portal: SailPortalFastApi, federation_id: str, dataset_id: str
    ):
        """
        Add a new dataset to a data federation.\n
        [PUT] /data-federations/{data_federation_id}/datasets/{dataset_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param federation_id: federation ID
        :type federation_id: str
        :param dataset_id: dataset ID
        :type dataset_id: str
        :return: response
        :rtype: string
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to update organization info
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/data-federations/{federation_id}/datasets/{dataset_id}",
                verify=False,
                headers=request_headers,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response

    def remove_dataset_from_data_federation(
        self, sail_portal: SailPortalFastApi, federation_id: str, dataset_id: str
    ):
        """
        Remove a dataset from a data federation.\n
        [DELETE] /data-federations/{data_federation_id}/datasets/{dataset_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param federation_id: data federation ID
        :type federation_id: str
        :param dataset_id: dataset ID
        :type dataset_id: str
        :return: response
        :rtype: string
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to delete an organization
        try:
            #  params as json
            response = requests.delete(
                f"{self.base_url}/data-federations/{federation_id}/datasets/{dataset_id}",
                verify=False,
                headers=request_headers,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response

    def get_existing_data_federation_dataset_key(
        self, sail_portal: SailPortalFastApi, federation_id: str, dataset_id: str
    ):
        """
        Get an existing dataset encryption key by retreiving and unwrapping.\n
        [GET] /data-federations/{data_federation_id}/dataset_key/{dataset_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param federation_id: federation ID
        :type federation_id: str
        :param dataset_id: dataset ID
        :type dataset_id: str
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        try:
            response = requests.get(
                f"{self.base_url}/data-federations/{federation_id}/dataset_key/{dataset_id}",
                headers=request_headers,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code
        return response, response.json()

    def get_or_create_data_federation_dataset_key(
        self,
        sail_portal: SailPortalFastApi,
        federation_id: str,
        dataset_id: str,
        create_if_not_found: str,
    ):
        """
        Get a dataset encryption key by either retreiving and unwrapping, or creating.\n
        [POST] /data-federations/{data_federation_id}/dataset_key/{dataset_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param federation_id: federation ID
        :type federation_id: str
        :param dataset_id: dataset ID
        :type dataset_id: str
        :param create_if_not_found: create a dataset key if none exists
        :type create_if_not_found: bool
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        try:
            response = requests.post(
                f"{self.base_url}/data-federations/{federation_id}/dataset_key/{dataset_id}?create_if_not_found={create_if_not_found}",
                headers=request_headers,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code
        return response, response.json()

    def provision_data_federation(
        self,
        sail_portal: SailPortalFastApi,
        federation_id: str,
        secure_comp_nodes_size: str,
    ):
        """
        Provision data federation SCNs.\n
        [POST] /data-federations-provisions

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param federation_id: data federation ID
        :type federation_id: str
        :param secure_comp_nodes_size: secure computation nodes size
        :type secure_comp_nodes_size: str
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        json_params = {
            "data_federation_id": federation_id,
            "secure_computation_nodes_size": secure_comp_nodes_size,
        }

        # Attempt to provision data federation
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/data-federations-provisions",
                verify=False,
                headers=request_headers,
                json=json_params,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response, response.json()

    def get_data_federation_provision_info(
        self, sail_portal: SailPortalFastApi, provision_id: str
    ):
        """
        Get data federation provision SCNs.\n
        [GET] /data-federations-provisions/{provision_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param provision_id: provision ID
        :type provision_id: str
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to provision data federation
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/data-federations-provsions/{provision_id}",
                verify=False,
                headers=request_headers,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response, response.json()

    def get_all_data_federation_provision_info(self, sail_portal: SailPortalFastApi):
        """
        Get all data federation provision SCNs.\n
        [GET] /data-federations-provisions

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to provision data federation
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/data-federations-provsions",
                verify=False,
                headers=request_headers,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response, response.json()

    def deprovision_data_federation(
        self, sail_portal: SailPortalFastApi, provision_id: str
    ):
        """
        Deprovision data federation SCNs.\n
        [DELETE] /data-federations-provisions/{provision_id}

        :param sail_portal: Fixture, SailPortalFastApi
        :type sail_portal: SailPortalFastApi
        :param provision_id: provision ID
        :type provision_id: str
        :return: response
        :rtype: string
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get(
            "access_token"
        )
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to provision data federation
        try:
            #  params as json
            response = requests.delete(
                f"{self.base_url}/data-federations-provisions/{provision_id}",
                verify=False,
                headers=request_headers,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        return response


class DataFederationManagementApi:
    """
    Data Federation Management Api Class
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

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
