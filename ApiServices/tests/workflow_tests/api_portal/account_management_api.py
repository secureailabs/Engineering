# -----------------------------------------------------------
#
# Class AccountManagementApi
#
# -----------------------------------------------------------
import requests
from tests.workflow_tests.api_portal.sail_portal_api import SailPortalApi
from tests.workflow_tests.utils.helpers import get_response_values, url_encoded


class AccountManagementFastApi:
    """
    Account Management FastApi Class
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # TODO Move to account_managment.py
    def get_current_user_info(self, sail_portal):
        """
        Get current User Information

        :return: _description_
        :rtype: _type_
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get("access_token")
        headers = {"Authorization": f"Bearer {authed_user_access_token}", "Accept": "application/json"}
        try:
            response = requests.get(f"{self.base_url}/me", headers=headers, verify=False)
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        return response, response.json()

    # TODO Move to account_managment.py
    def get_all_organization_info(self, sail_portal):
        """
        SAIL_ACTOR resticted get all organizations

        :return: _description_
        :rtype: _type_
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get("access_token")
        headers = {"Authorization": f"Bearer {authed_user_access_token}", "Accept": "application/json"}
        try:
            response = requests.get(f"{self.base_url}/organizations", headers=headers, verify=False)
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        return response, response.json()

    # TODO Move to account_managment.py
    def get_current_user_organization_info(self, sail_portal):
        """
        Get current User Organization Information

        :return: _description_
        :rtype: _type_
        """
        authed_user_access_token = sail_portal.login_for_access_token()[1].get("access_token")
        headers = {"Authorization": f"Bearer {authed_user_access_token}", "Accept": "application/json"}
        current_user_org_id = (
            requests.get(f"{self.base_url}/me", headers=headers, verify=False).json()["organization"].get("id")
        )
        try:
            response = requests.get(
                f"{self.base_url}/organizations/{current_user_org_id}", headers=headers, verify=False
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        return response, response.json()


class AccountManagementApi:
    """
    Account Management Api Class
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def get_user_organization_info(self, sail_portal):
        """
        Get User Organization Info

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :return: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        _, _, user_eosb = sail_portal.login()
        # query_params = url_encoded({"Eosb": user_eosb})
        json_params = {"Eosb": user_eosb}
        # Attempt to get user organization info
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/SAIL/AccountManager/Organization/Information", json=json_params, verify=False
            )
            # params query string
            # response = requests.get(
            #     f"{self.base_url}/SAIL/AccountManager/Organization/Information", params=query_params, verify=False
            # )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def update_user_organization_info(self, sail_portal, payload):
        """
        Update User Organization Info

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        _, user_info_json, user_eosb = sail_portal.get_basic_user_info()
        org_guid = user_info_json.get("OrganizationGuid")
        json_params = {"Eosb": user_eosb, "OrganizationGuid": org_guid}
        json_params.update(payload)
        # Attempt to update user organization info
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/SAIL/AccountManager/Update/Organization",
                json=json_params,
                headers=self.headers,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def update_user_access_rights(self, sail_portal):
        """
        Update User Access rights

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :return: response, response.json()
        :rtype: (string, string)
        """
        _, user_info_json, user_eosb = sail_portal.get_basic_user_info()
        user_guid = user_info_json.get("UserGuid")
        json_params = {"Eosb": user_eosb, "UserGuid": user_guid, "AccessRights": 1}
        # Attempt to update user access rights
        try:
            response = requests.put(
                f"{self.base_url}/SAIL/AccountManager/Update/AccessRight",
                json=json_params,
                headers=self.headers,
                verify=False,
            )
        except requests.exceptions.HTTPError as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def list_organization_users(self, sail_portal):
        """
        Update User Access rights

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi]
        :return: response, response.json()
        :rtype: (string, string)
        """
        _, user_info_json, user_eosb = sail_portal.get_basic_user_info()
        user_org_guid = user_info_json.get("OrganizationGuid")
        json_params = {"Eosb": user_eosb, "OrganizationGuid": user_org_guid}
        # Attempt to list_organization_users
        try:
            response = requests.get(
                f"{self.base_url}/SAIL/AccountManager/Organization/Users",
                json=json_params,
                headers=self.headers,
                verify=False,
            )
        except requests.exceptions.HTTPError as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def update_user_information(self, sail_portal, payload):
        """
        Update User Information

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        _, user_info_json, user_eosb = sail_portal.get_basic_user_info()
        user_guid = user_info_json.get("UserGuid")
        json_params = {"Eosb": user_eosb, "UserGuid": user_guid}
        json_params.update(payload)
        # Attempt to update user organization info
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/SAIL/AccountManager/Update/User",
                json=json_params,
                headers=self.headers,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def add_user(self, sail_portal, payload):
        """
        Add Register new user into database

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :param payload: url payload
        :type payload: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        _, user_info_json, user_eosb = sail_portal.get_basic_user_info()
        user_org_guid = user_info_json.get("OrganizationGuid")
        json_params = {"Eosb": user_eosb, "OrganizationGuid": user_org_guid}
        json_params.update(payload)
        query_params = url_encoded(json_params)
        try:
            #  params as json
            # response = requests.post(
            #     f"{self.base_url}/SAIL/AccountManager/Admin/RegisterUser",
            #     json=json_params,
            #     headers=self.headers,
            #     verify=False,
            # )
            response = requests.post(
                f"{self.base_url}/SAIL/AccountManager/Admin/RegisterUser",
                params=query_params,
                headers=self.headers,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def delete_user(self, sail_portal, get_base_url, Email, Password):
        """
        Delete user from database

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :return: response, response.json()
        :rtype: (string, string)
        """
        # Get user id of user to be deleted
        sail_portal1 = SailPortalApi(base_url=get_base_url, email=Email, password=Password)
        _, user_info_json, user_eosb = sail_portal1.get_basic_user_info()
        user_guid = user_info_json.get("UserGuid")
        json_params = {"Eosb": user_eosb, "UserGuid": user_guid}
        # Login as primary admin user
        sail_portal.login()
        # query_params = url_encoded(json_params)
        try:
            #  params as json
            #  Delete user
            response = requests.delete(
                f"{self.base_url}/SAIL/AccountManager/Remove/User",
                json=json_params,
                headers=self.headers,
                verify=False,
            )
            # query_response = requests.delete(
            #     f"{self.base_url}/SAIL/AccountManager/Remove/User",
            #     params=query_params,
            #     headers=self.headers,
            #     verify=False,
            # )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, user guid and user eosb
        return (*get_response_values(response), user_guid)

    def recover_user(self, user_eosb, user_guid):
        """
        Recover user into database

        :param sail_portal: fixture, SailPortalApi
        :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
        :return: response, response.json()
        :rtype: (string, string)
        """
        json_params = {"Eosb": user_eosb, "UserGuid": user_guid}
        # query_params = url_encoded(json_params)
        try:
            response = requests.put(
                f"{self.base_url}/SAIL/AccountManager/Update/RecoverUser",
                json=json_params,
                headers=self.headers,
                verify=False,
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)
