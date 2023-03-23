# -------------------------------------------------------------------------------
# Engineering
# account_management_api_test.py
# -------------------------------------------------------------------------------
"""Account Management Api Tests"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
import pytest
from assertpy.assertpy import assert_that
from cerberus import Validator

# from app.models.accounts import GetOrganizations_Out, UserInfo_Out
from tests.workflow_tests.api_portal.sail_portal_api import SailPortalApi
from tests.workflow_tests.config import SAIL_PASS
from tests.workflow_tests.utils.account_helpers import get_add_user_payload
from tests.workflow_tests.utils.helpers import pretty_print


def debug_helper(response):
    print(f"\n----------HELLO------------")
    print(f"{response.url}")
    print(f"------------END--------------")


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal",
    [
        "data_owner_sail_fast_api_portal",
        "researcher_sail_fast_api_portal",
    ],
)
def test_get_current_user_info(sail_portal, account_management_fast_api, request):
    """

    :param sail_portal: sailportal
    :type sail_portal: object
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "job_title": {"type": "string"},
        "role": {"type": "string"},
        "avatar": {"required": False, "nullable": True, "type": "string"},
        "id": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
    }
    validator = Validator(schema)
    # Act
    test_response, test_response_json = account_management_fast_api.get_current_user_info(sail_portal)
    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)
    # assert_that(UserInfo_Out(**test_response_json))


# TODO BROKEN : "detail": "Operation not permitted" requires SAIL_ACTOR
@pytest.mark.broken
@pytest.mark.parametrize(
    "sail_portal",
    [
        "data_owner_sail_fast_api_portal",
        "researcher_sail_fast_api_portal",
    ],
)
def test_get_list_organizations_info(sail_portal, account_management_fast_api, request):
    """
    SAIL ACTOR get list of all organizations
    :param sail_portal: _description_
    :type sail_portal: _type_
    :param request: _description_
    :type request: _type_
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "organizations": {
            "type": "dict",
            "schema": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "avatar": {"required": False, "nullable": True, "type": "string"},
                "id": {"type": "string"},
            },
        },
    }
    validator = Validator(schema)
    # Act
    test_response, test_response_json = account_management_fast_api.get_all_organization_info(sail_portal)
    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal",
    [
        "data_owner_sail_fast_api_portal",
        "researcher_sail_fast_api_portal",
    ],
)
def test_get_current_user_organization_info(sail_portal, account_management_fast_api, request):
    """
    Test gets current authenticated user organization information

    :param sail_portal: sail_portal
    :type sail_portal: object
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "avatar": {"required": False, "nullable": True, "type": "string"},
        "id": {"type": "string"},
    }
    validator = Validator(schema)
    # Act
    test_response, test_response_json = account_management_fast_api.get_current_user_organization_info(sail_portal)
    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)
    # assert_that(GetOrganizations_Out(**test_response_json))


# * -------------------------------------------------------------- OLD API BELOW --------------------------------------------------------------
# ! -------------------------------------------------------------- OLD API BELOW --------------------------------------------------------------
# ? -------------------------------------------------------------- OLD API BELOW --------------------------------------------------------------
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_get_user_organization_info(sail_portal, account_management, request):
    """
    Testing getting of Organization information

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param account_management: fixture, account_management
    :type account_management: api_portal.account_management_api.AccountManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "Eosb": {"type": "string"},
        "OrganizationInformation": {
            "type": "dict",
            "schema": {
                "OrganizationAddress": {"type": "string"},
                "OrganizationName": {"type": "string"},
                "PrimaryContactEmail": {"type": "string"},
                "PrimaryContactName": {"type": "string"},
                "PrimaryContactPhoneNumber": {"type": "string"},
                "PrimaryContactTitle": {"type": "string"},
                "SecondaryContactEmail": {"type": "string"},
                "SecondaryContactName": {"type": "string"},
                "SecondaryContactPhoneNumber": {"type": "string"},
                "SecondaryContactTitle": {"type": "string"},
            },
        },
        "Status": {"type": "number"},
    }
    validator = Validator(schema)

    # Act
    test_response, test_response_json, user_eosb = account_management.get_user_organization_info(sail_portal)
    # user_guid = test_response.json().get("UserGuid")
    pretty_print("Test Response:", test_response_json)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_update_organization_information(sail_portal, account_management, request):
    """
    Testing update of organization information

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param account_management: fixture, account_management
    :type account_management: api_portal.account_management_api.AccountManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)
    test_payload = {
        "OrganizationInformation": {
            "OrganizationName": "Raptors12345",
            "OrganizationAddress": "Jurasic12345",
            "PrimaryContactName": "Masai",
            "PrimaryContactTitle": "VP",
            "PrimaryContactEmail": "masai@raptors.com",
            "PrimaryContactPhoneNumber": "123123123",
            "SecondaryContactName": "Boby",
            "SecondaryContactTitle": "Exec",
            "SecondaryContactEmail": "bobby@raptors.com",
            "SecondaryContactPhoneNumber": "321321321",
        }
    }
    # Act
    test_response, test_response_json, user_eosb = account_management.update_user_organization_info(
        sail_portal, payload=test_payload
    )
    # Assert
    # Get user organization info to verify results
    _, user_org_info_json, _ = account_management.get_user_organization_info(sail_portal)
    pretty_print("Verify updated Organization information:", user_org_info_json)
    # Verify updated information
    for key in test_payload:
        value = test_payload[key]
        temp = user_org_info_json.get("OrganizationInformation")
        for key in value:
            new_value = value[key]
            assert (key, new_value) in temp.items()
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


# TODO create new user and cycle through user rights
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_update_user_access_rights(sail_portal, account_management, request):
    """
    Validates updates to user access rights
    # eAdmin=1,
    # eAuditor=2,
    # eOrganizationUser=3,
    # eDigitalContractAdmin=4,
    # eDatasetAdmin=5,
    # eSailAdmin=6

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param account_management: fixture, account_management
    :type account_management: api_portal.account_management_api.AccountManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)

    # Act
    test_response, test_response_json, user_eosb = account_management.update_user_access_rights(sail_portal)

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_list_organization_users(sail_portal, account_management, request):
    """
    Validate list of organization users

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param account_management: fixture, account_management
    :type account_management: api_portal.account_management_api.AccountManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "Eosb": {"type": "string"},
        "OrganizationUsers": {
            "type": "dict",
            "valueschema": {
                "type": "dict",
                "schema": {
                    "AccessRights": {"type": "number"},
                    "AccountStatus": {"type": "number"},
                    "Email": {"type": "string"},
                    "PhoneNumber": {"type": "string"},
                    "TimeOfAccountCreation": {"type": "number"},
                    "Title": {"type": "string"},
                    "UserGuid": {"type": "string"},
                    "Username": {"type": "string"},
                },
            },
        },
        "Status": {"type": "number"},
    }
    validator = Validator(schema)

    # Act
    test_response, test_response_json, user_eosb = account_management.list_organization_users(sail_portal)

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_update_user_information(sail_portal, account_management, request):
    """
    Testing update of organization information

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param account_management: fixture, account_management
    :type account_management: api_portal.account_management_api.AccountManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)
    test_payload = {
        "UserInformation": {
            "Name": "lowry",
            "Title": "GR1OATY",
            "PhoneNumber": "4443331234",
        }
    }

    # Act
    test_response, test_response_json, user_eosb = account_management.update_user_information(
        sail_portal, payload=test_payload
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_add_user(sail_portal, get_base_url, account_management, request):
    """
    Testing add user to database

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param account_management: fixture, account_management
    :type account_management: api_portal.account_management_api.AccountManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)

    # Act
    test_payload, user_email = get_add_user_payload()
    test_response, test_response_json, user_eosb = account_management.add_user(sail_portal, payload=test_payload)
    # validate login of new user
    _sail_portal = SailPortalApi(base_url=get_base_url, email=user_email, password=SAIL_PASS)
    _test_response, _, _ = _sail_portal.get_basic_user_info()

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(201)
    assert_that(_test_response.status_code).is_equal_to(200)


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_delete_user(sail_portal, account_management, get_base_url, request):
    """
    Testing delete user from database

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param account_management: fixture, account_management
    :type account_management: api_portal.account_management_api.AccountManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)
    test_payload, user_email = get_add_user_payload()
    account_management.add_user(sail_portal, payload=test_payload)

    # Act
    test_response, test_response_json, user_eosb, _ = account_management.delete_user(
        sail_portal, get_base_url, Email=user_email, Password=SAIL_PASS
    )
    # Verify deleted user cannot login
    _sail_portal = SailPortalApi(base_url=get_base_url, email=user_email, password=SAIL_PASS)
    _test_response, _, _ = _sail_portal.get_basic_user_info()
    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)
    assert_that(_test_response.status_code).is_equal_to(400)


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_recover_user(sail_portal, account_management, get_base_url, request):
    """
    Testing recover user from database

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param account_management: fixture, account_management
    :type account_management: api_portal.account_management_api.AccountManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)
    test_payload, user_email = get_add_user_payload()
    account_management.add_user(sail_portal, payload=test_payload)
    _, _, deleted_user_eosb, deleted_user_guid = account_management.delete_user(
        sail_portal, get_base_url, Email=user_email, Password=SAIL_PASS
    )
    # Act
    test_response, test_response_json, user_eosb = account_management.recover_user(
        user_eosb=deleted_user_eosb, user_guid=deleted_user_guid
    )
    # Verify recover user can login
    _sail_portal = SailPortalApi(base_url=get_base_url, email=user_email, password=SAIL_PASS)
    _test_response, _, _ = _sail_portal.get_basic_user_info()
    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)
    assert_that(_test_response.status_code).is_equal_to(200)
