# -------------------------------------------------------------------------------
# Engineering
# sail_portal_api.py
# -------------------------------------------------------------------------------
"""Sail Portal Api Module"""
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
from tests.workflow_tests.utils.organization_helper import Organization, User


class SailPortalFastApi:
    """
    Sail Portal Fast Api Class
    """

    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def login_for_access_token(self):
        """
        Login to Sail Api portal.\n
        [POST] /login

        :returns: response, response.json()
        :rtype: (string, string)
        """
        payload = f"username={self.email}&password={self.password}"
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}

        try:
            response = requests.post(f"{self.base_url}/login", headers=headers, data=payload, verify=False)
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code
        return response, response.json()

    def get_refresh_token(self):
        """
        Refresh the JWT token for the user.\n
        [POST] /refresh-token

        :returns: response, response.json()
        :rtype: (string, string)
        """
        authed_user_refresh_token = self.login_for_access_token()[1].get("refresh_token")
        payload = {"refresh_token": f"{authed_user_refresh_token}"}

        try:
            response = requests.post(f"{self.base_url}/refresh-token", headers=self.headers, json=payload, verify=False)
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code
        return response, response.json()

    def get_basic_user_info(self):
        """
        Get basic user information for the logged in user.\n
        [GET] /me

        :returns: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = self.login_for_access_token()[1].get("access_token")
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        try:
            response = requests.get(f"{self.base_url}/me", headers=request_headers, verify=False)
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code
        return response, response.json()

    # TODO: Evaluate this function after permissioned user is created.
    def get_all_organizations(self):
        """
        Get all organizations.\n
        [GET] /organizations

        :returns: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = self.login_for_access_token()[1].get("access_token")
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        try:
            response = requests.get(f"{self.base_url}/organizations", headers=request_headers, verify=False)
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code
        return response, response.json()

    def get_organization_by_id(self, org_id: str):
        """
        Get an organization by ID using the sail portal API.\n
        [GET] /organizations/{organization_id}

        :param org_id: organization ID
        :type org_id: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = self.login_for_access_token()[1].get("access_token")
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to get an organization by ID
        try:
            #  params as json
            response = requests.get(f"{self.base_url}/organizations/{org_id}", verify=False, headers=request_headers)
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response, response.json()

    def register_new_organization(self, new_org: Organization):
        """
        Register a new organization using the Sail Api portal.\n
        [POST] /organizations

        :param new_org: organization object
        :type new_org: object
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = self.login_for_access_token()[1].get("access_token")
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        json_params = {
            "name": new_org.name,
            "description": new_org.description,
            "avatar": new_org.avatar,
            "admin_name": new_org.admin_name,
            "admin_job_title": new_org.admin_job_title,
            "admin_email": new_org.admin_email,
            "admin_password": new_org.admin_password,
            "admin_avatar": new_org.admin_avatar,
        }

        # Attempt to register a new organization
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/organizations", verify=False, headers=request_headers, json=json_params
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response, response.json()

    def update_organization_info(self, org_id: str, new_name: str, new_description: str, new_avatar: str):
        """
        Update organization information using the Sail Api portal.\n
        [PUT] /organizations/{organization_id}

        :param org_id: organization ID
        :type org_id: string
        :param new_name: new name of organization
        :type new_name: string
        :param new_description: new description of organization
        :type new_description: string
        :param new_avatar: new avatar of organization
        :type new_avatar: string
        :return: response
        :rtype: string
        """
        authed_user_access_token = self.login_for_access_token()[1].get("access_token")
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        json_params = {
            "name": new_name,
            "description": new_description,
            "avatar": new_avatar,
        }

        # Attempt to update organization info
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/organizations/{org_id}", verify=False, headers=request_headers, json=json_params
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response

    def delete_organization(self, org_id: str):
        """
        Delete an organization using the Sail Api portal.\n
        [DELETE] /organizations/{organization_id}

        :param org_id: organization ID
        :type org_id: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = self.login_for_access_token()[1].get("access_token")
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to delete an organization
        try:
            #  params as json
            response = requests.delete(f"{self.base_url}/organizations/{org_id}", verify=False, headers=request_headers)
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response, response.json()

    def get_organization_users(self, org_id: str):
        """
        Get users of an organization using the Sail Api portal.\n
        [GET] /organizations/{organization_id}/users

        :param org_id: organization ID
        :type org_id: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = self.login_for_access_token()[1].get("access_token")
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to get an organizations users
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/organizations/{org_id}/users", verify=False, headers=request_headers
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response, response.json()

    def register_new_user_to_organization(self, org_id: str, new_user: User):
        """
        Register a new user to an organization using the Sail Api portal.\n
        [POST] /organizations/{organization_id}/users/{user_id}

        :param org_id: organization ID
        :type org_id: string
        :param new_user: new user object
        :type new_user: object
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = self.login_for_access_token()[1].get("access_token")
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        json_params = {
            "name": new_user.name,
            "email": new_user.email,
            "job_title": new_user.job_title,
            "role": new_user.role,
            "avatar": new_user.avatar,
            "password": new_user.password,
        }

        # Attempt to register a new user to the organization
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/organizations/{org_id}/users", verify=False, headers=request_headers, json=json_params
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response, response.json()

    def get_organization_user_by_id(self, org_id: str, user_id: str):
        """
        Get user of an organization by ID using the Sail Api portal.\n
        [GET] /organizations/{organization_id}/users/{user_id}

        :param org_id: organization ID
        :type org_id: string
        :param user_id: user ID
        :type user_id: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = self.login_for_access_token()[1].get("access_token")
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to get organization user by ID
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/organizations/{org_id}/users/{user_id}", verify=False, headers=request_headers
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response, response.json()

    def update_organization_user(
        self, org_id: str, user_id: str, new_job_title: str, new_role: str, new_account_state: str, new_avatar: str
    ):
        """
        Update user of an organization by ID using the Sail Api portal.\n
        [PUT] /organizations/{organizations_id}/users/{user_id}

        :param org_id: organization ID
        :type org_id: string
        :param user_id: user ID
        :type user_id: string
        :param new_job_title: user new job title
        :type new_job_title: string
        :param new_role: user new role
        :type new_role: string
        :param new_account_state: user new account state
        :type new_account_state: string
        :param new_avatar: user new avatar
        :type new_avatar: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = self.login_for_access_token()[1].get("access_token")
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        json_params = {
            "job_title": new_job_title,
            "role": new_role,
            "account_state": new_account_state,
            "avatar": new_avatar,
        }

        # Attempt to update organization user info
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/organizations/{org_id}/users/{user_id}",
                verify=False,
                headers=request_headers,
                json=json_params,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response

    def delete_organization_user_by_id(self, org_id: str, user_id: str):
        """
        Delete an organization user using the Sail Api portal.\n
        [DELETE] /organizations/{organizations_id}/users/{user_id}

        :param org_id: organization ID
        :type org_id: string
        :param user_id: user ID
        :type user_id: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        authed_user_access_token = self.login_for_access_token()[1].get("access_token")
        request_headers = {"Authorization": f"Bearer {authed_user_access_token}"}

        # Attempt to delete user from organization
        try:
            #  params as json
            response = requests.delete(
                f"{self.base_url}/organizations/{org_id}/users/{user_id}", verify=False, headers=request_headers
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return response


class SailPortalApi:
    """
    Sail Portal Api Class
    """

    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # TODO Remote Attestation Certificate

    def login(self):
        """
        Login to Sail Api portal

        :returns: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        json_params = {"Email": self.email, "Password": self.password}
        # query_params = url_encoded({"Email": self.email, "Password": self.password})
        # Attempt to login to SAIL PORTAL via POST request
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/SAIL/AuthenticationManager/User/Login", json=json_params, verify=False
            )
            # params query string
            # response = requests.post(
            #     f"{self.base_url}/SAIL/AuthenticationManager/User/Login", params=query_params, verify=False
            # )
            # response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output and user eosb
        return get_response_values(response)

    def get_basic_user_info(self):
        """
        Get basic user information from  Sail Api portal

        :return: response, response.json()
        :rtype: (string, string)
        """
        _, _, user_eosb = self.login()
        json_params = {"Eosb": user_eosb}
        # query_params = url_encoded({"Eosb": user_eosb})
        # Attempt to get basic user information
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/SAIL/AuthenticationManager/GetBasicUserInformation", json=json_params, verify=False
            )
            # params query string
            # response = requests.get(
            #     f"{self.base_url}/SAIL/AuthenticationManager/GetBasicUserInformation", params=query_params, verify=False
            # )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def update_password(self, current_password, new_password):
        """
        Get update user password from  Sail Api portal

        :param current_password:
        :type current_password: string
        :param new_password:
        :type new_password: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        self.password = current_password
        _, _, user_eosb = self.login()
        #  params as json
        json_params = {
            "Eosb": user_eosb,
            "Email": self.email,
            "CurrentPassword": current_password,
            "NewPassword": new_password,
        }
        # query_params = url_encoded(
        #     {"Eosb": user_eosb, "Email": self.email, "CurrentPassword": current_password, "NewPassword": new_password}
        # )
        # Attempt to update user password
        try:
            #  params as json
            response = requests.patch(
                f"{self.base_url}/SAIL/AuthenticationManager/User/Password", json=json_params, verify=False
            )
            # params query string
            # response = requests.patch(
            #     f"{self.base_url}/SAIL/AuthenticationManager/User/Password", params=query_params, verify=False
            # )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def check_eosb(self, eosb):
        """
        Call the CheckEosb API in the Sail portal

        :param eosb:
        :type eosb: string
        :param new_password:
        :type new_password: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, user_eosb)
        """
        #  params as json
        json_params = {"Eosb": eosb}
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/SAIL/AuthenticationManager/CheckEosb", json=json_params, verify=False
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return get_response_values(response)
