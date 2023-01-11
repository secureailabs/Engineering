# -------------------------------------------------------------------------------
# Engineering
# datafederation_management_api_test.py
# -------------------------------------------------------------------------------
"""Data Federation Management Test Module"""
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
from tests.workflow_tests.api_portal.datafederation_management_api import (
    DataFederationManagementFastApi,
)
from tests.workflow_tests.api_portal.dataset_management_api import (
    DataSetManagementFastApi,
)
from tests.workflow_tests.api_portal.sail_portal_api import SailPortalFastApi
from tests.workflow_tests.utils.dataset_helpers import Dataset
from tests.workflow_tests.utils.federation_helpers import DataFederation
from tests.workflow_tests.utils.helpers import random_name
from tests.workflow_tests.utils.organization_helper import Organization


def print_response_values(function_name, response, response_json):
    print(
        f"\n\n============================================================{function_name}============================================================"
    )
    print(f"Test Response: {response}\n")
    print(f"Test Response JSON: {response_json}\n")
    print(
        f"============================================================{function_name}============================================================\n"
    )


def print_federation_data(federation):
    organization = federation.get("organization")
    data_submitter_organizations = f""
    for submitter in federation.get("data_submitter_organizations"):
        data_submitter_organizations += (
            f"\n|\t\tName:\t{submitter.get('name')}\n|\t\tID:\t{submitter.get('id')}\n|"
        )
    research_organizations = f""
    for researcher in federation.get("research_organizations"):
        research_organizations += f"\n|\t\t|Name:\t{researcher.get('name')}\n|\t\tID:\t{researcher.get('id')}\n|"
    dataset_list = f""
    for dataset_list_element in federation.get("datasets"):
        dataset_list += f"\n|\t\tName:\t{dataset_list_element.get('name')}\n|\t\tID:\t{dataset_list_element.get('id')}\n|"
    data_submitter_invite_list = f""
    for data_submitter_invite in federation.get(
        "data_submitter_organizations_invites_id"
    ):
        data_submitter_invite_list += f"\n|\tID:\t{data_submitter_invite}\n|"
    research_invite_list = f""
    for research_invite in federation.get("research_organizations_invites_id"):
        research_invite_list += f"\n|\tID:\t{research_invite}\n|"
    print(
        f"\n\n|Federation Name:\t\t{federation.get('name')}\n\
|Description:\t\t\t{federation.get('description')}\n\
|ID:\t\t\t\t{federation.get('id')}\n\
|Data Format:\t\t\t{federation.get('data_format')}\n\
|Creation Time:\t\t\t{federation.get('creation_time')}\n\
|Organization Name:\t\t{organization.get('name')}\n\
|Organization ID:\t\t{organization.get('id')}\n\
|State:\t\t\t\t{federation.get('state')}\n\
|Data Submitter Organizations:\t{data_submitter_organizations}\n\
|Research Organizations:\t{research_organizations}\n\
|Datasets:\t\t\t{dataset_list}\n\
|Data Submitter Organizations Invites ID:\t{data_submitter_invite_list}\n\
|Research Organizations Invites ID:\t{research_invite_list}"
    )


def get_federation(sail_portal: SailPortalFastApi, federation_management: DataFederationManagementFastApi):
    federation = None
    for new_federation in pytest.new_federations:
        if new_federation.get("admin_email") == sail_portal.email:
            _, federation = federation_management.get_data_federation_by_id(
                sail_portal, new_federation.get("id")
            )
            break

    if federation is None:
        _, federations_json = federation_management.get_all_data_federations(
            sail_portal
        )
        federation = federations_json.get("data_federations")[
            len(federations_json.get("data_federations")) - 1
        ]

    return federation


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
    ],
)
def test_fastapi_get_all_data_federations(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    request,
):
    """
    Test getting all data federations associated with the users organization.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "data_federations": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = federation_management.get_all_data_federations(
        sail_portal
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, new_federation",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "create_valid_data_federation",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "create_valid_data_federation",
        ),
    ],
)
def test_fastapi_register_valid_data_federation(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    new_federation: DataFederation,
    request,
):
    """
    Test registering a new valid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param new_federation: new federation object
    :type new_federation: DataFederation
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    new_federation = request.getfixturevalue(new_federation)

    schema = {
        "id": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = federation_management.register_data_federation(
        sail_portal, new_federation
    )

    pytest.new_federations.append(
        {
            "admin_email": sail_portal.email,
            "admin_pass": sail_portal.password,
            "id": test_response_json.get("id"),
        }
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(201)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, new_federation",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "create_invalid_data_federation",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "create_invalid_data_federation",
        ),
    ],
)
def test_fastapi_register_invalid_data_federation(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    new_federation: DataFederation,
    request,
):
    """
    Test registering a new invalid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param new_federation: new federation object
    :type new_federation: DataFederation
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    new_federation = request.getfixturevalue(new_federation)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = federation_management.register_data_federation(
        sail_portal, new_federation
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management",
    [
        ("data_owner_sail_fast_api_portal", "datafederation_management_fast_api"),
        ("researcher_sail_fast_api_portal", "datafederation_management_fast_api"),
    ],
)
def test_fastapi_get_valid_data_federation(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    request,
):
    """
    Test getting a valid data federation by ID.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "data_format": {"type": "string"},
        "id": {"type": "string"},
        "creation_time": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
        "state": {"type": "string"},
        "data_submitter_organizations": {"type": "list"},
        "research_organizations": {"type": "list"},
        "datasets": {"type": "list"},
        "data_submitter_organizations_invites_id": {"type": "list"},
        "research_organizations_invites_id": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    for federation in federations_json.get("data_federations"):
        (
            test_response,
            test_response_json,
        ) = federation_management.get_data_federation_by_id(
            sail_portal, federation.get("id")
        )

        # Assert
        is_valid = validator.validate(test_response_json)
        assert_that(is_valid, description=validator.errors).is_true()
        assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_federation_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_get_invalid_data_federation(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_federation_id: str,
    request,
):
    """
    Test getting an invalid data federation by using an invalid federation ID.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_federation_id: invalid federation ID
    :type invalid_federation_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = federation_management.get_data_federation_by_id(
        sail_portal, invalid_federation_id
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, new_name, new_description",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"Test Update Name-{random_name(4)}",
            f"This is an updated Test Data Federation Description-{random_name(4)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"Test Update Name-{random_name(4)}",
            f"This is an updated Test Data Federation Description-{random_name(4)}",
        ),
    ],
)
def test_fastapi_update_valid_data_federation_authorized_user(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    new_name: str,
    new_description: str,
    request,
):
    """
    Test updating a valid data federation by an authorized user.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param new_name: new name
    :type new_name: str
    :param new_description: new description
    :type new_description: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    payload = {
        "name": new_name,
        "description": new_description,
    }

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "data_format": {"type": "string"},
        "id": {"type": "string"},
        "creation_time": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
        "state": {"type": "string"},
        "data_submitter_organizations": {"type": "list"},
        "research_organizations": {"type": "list"},
        "datasets": {"type": "list"},
        "data_submitter_organizations_invites_id": {"type": "list"},
        "research_organizations_invites_id": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    federation = get_federation(sail_portal, federation_management)

    original_federation = DataFederation(
        federation.get("name"),
        federation.get("description"),
        federation.get("data_format"),
    )

    test_response = federation_management.update_data_federation(
        sail_portal, federation.get("id"), payload=payload
    )

    (
        verify_response,
        verify_response_json,
    ) = federation_management.get_data_federation_by_id(
        sail_portal, federation.get("id")
    )

    # Assert
    is_valid = validator.validate(verify_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(verify_response_json.get("name")).is_equal_to(new_name)
    assert_that(verify_response_json.get("description")).is_equal_to(new_description)
    assert_that(test_response.status_code).is_equal_to(204)

    payload = {
        "name": original_federation.name,
        "description": original_federation.description,
    }

    revert_response = federation_management.update_data_federation(
        sail_portal, federation.get("id"), payload=payload
    )


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, sail_portal_target, federation_management, new_name, new_description",
    [
        (
            "data_owner_sail_fast_api_portal",
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            None,
            None,
        ),
        (
            "researcher_sail_fast_api_portal",
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            None,
            None,
        ),
    ],
)
def test_fastapi_update_valid_data_federation_unauthorized_user(
    sail_portal: SailPortalFastApi,
    sail_portal_target: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    new_name: str,
    new_description: str,
    request,
):
    """
    Test updating a valid data federation by an unauthorized user.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param sail_portal_target: Fixture
    :type sail_portal_target: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param new_name: new name
    :type new_name: str
    :param new_description: new description
    :type new_description: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    sail_portal_target = request.getfixturevalue(sail_portal_target)
    federation_management = request.getfixturevalue(federation_management)

    payload = {
        "name": new_name,
        "description": new_description,
    }

    schema = {
        "detail": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(
        sail_portal_target
    )
    federation = federations_json.get("data_federations")[
        len(federations_json.get("data_federations")) - 1
    ]
    original_federation = DataFederation(
        federation.get("name"),
        federation.get("description"),
        federation.get("data_format"),
    )

    test_response = federation_management.update_data_federation(
        sail_portal, federation.get("id"), payload=payload
    )

    _, verify_response_json = federation_management.get_data_federation_by_id(
        sail_portal_target, federation.get("id")
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(verify_response_json.get("name")).is_equal_to(original_federation.name)
    assert_that(verify_response_json.get("description")).is_equal_to(
        original_federation.description
    )
    assert_that(test_response.status_code).is_equal_to(403)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, federation_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_update_invalid_data_federation(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    federation_id: str,
    request,
):
    """
    Test updating an invalid data federation using an invalid ID.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param federation_id: federation ID
    :type federation_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    payload = {
        "name": random_name(16),
        "description": random_name(16),
    }

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response = federation_management.update_data_federation(
        sail_portal, federation_id, payload=payload
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, new_organization",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "create_valid_organization",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "create_valid_organization",
        ),
    ],
)
def test_fastapi_valid_data_federation_register_valid_researcher(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    new_organization: Organization,
    request,
):
    """
    Test registering a valid researcher organization to a valid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param new_organization: new organization
    :type new_organization: Organization
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    new_organization = request.getfixturevalue(new_organization)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "data_format": {"type": "string"},
        "id": {"type": "string"},
        "creation_time": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
        "state": {"type": "string"},
        "data_submitter_organizations": {"type": "list"},
        "research_organizations": {"type": "list"},
        "datasets": {"type": "list"},
        "data_submitter_organizations_invites_id": {"type": "list"},
        "research_organizations_invites_id": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    federation = get_federation(sail_portal, federation_management)

    (
        reg_new_org_response,
        reg_new_org_response_json,
    ) = sail_portal.register_new_organization(new_organization)

    pytest.new_organizations.append(
        {
            "admin_email": new_organization.admin_email,
            "admin_pass": new_organization.admin_password,
            "id": reg_new_org_response_json.get("id"),
        }
    )

    test_response = federation_management.register_researcher_to_data_federation(
        sail_portal, federation.get("id"), reg_new_org_response_json.get("id")
    )

    (
        new_fed_response,
        new_fed_response_json,
    ) = federation_management.get_data_federation_by_id(
        sail_portal, federation.get("id")
    )

    research_organizations = new_fed_response_json.get("research_organizations")
    is_added = False
    for org in research_organizations:
        if org.get("id") == reg_new_org_response_json.get("id"):
            is_added = True
            break

    # Assert
    is_valid = validator.validate(new_fed_response_json)
    assert_that(is_added).is_true()
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(204)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_org_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_valid_data_federation_register_invalid_researcher(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_org_id: str,
    request,
):
    """
    Test registering an invalid researcher organization to a valid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_org_id: invalid organization ID
    :type invalid_org_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    federation = federations_json.get("data_federations")[
        len(federations_json.get("data_federations")) - 1
    ]

    test_response = federation_management.register_researcher_to_data_federation(
        sail_portal, federation.get("id"), invalid_org_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, sail_portal_target, federation_management, invalid_federation_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_invalid_data_federation_register_valid_researcher(
    sail_portal: SailPortalFastApi,
    sail_portal_target: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_federation_id: str,
    request,
):
    """
    Test registering a valid researcher organization to an invalid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param sail_portal_target: Fixture
    :type sail_portal_target: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_federation_id: invalid federation ID
    :type invalid_federation_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    sail_portal_target = request.getfixturevalue(sail_portal_target)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    user_response, user_response_json = sail_portal_target.get_basic_user_info()
    target_org = user_response_json.get("organization")

    test_response = federation_management.register_researcher_to_data_federation(
        sail_portal, invalid_federation_id, target_org.get("id")
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_federation_id, invalid_org_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_invalid_data_federation_register_invalid_researcher(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_federation_id: str,
    invalid_org_id: str,
    request,
):
    """
    Test registering an invalid researcher organization to an invalid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_federation_id: invalid federation ID
    :type invalid_federation_id: str
    :param invalid_org_id: invalid organization ID
    :type invalid_org_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response = federation_management.register_researcher_to_data_federation(
        sail_portal, invalid_federation_id, invalid_org_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, new_organization",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "create_valid_organization",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "create_valid_organization",
        ),
    ],
)
def test_fastapi_valid_data_federation_register_valid_data_submitter(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    new_organization: Organization,
    request,
):
    """
    Test registering a valid data submitter organization to a valid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param new_organization: new organization
    :type new_organization: Organization
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    new_organization = request.getfixturevalue(new_organization)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "data_format": {"type": "string"},
        "id": {"type": "string"},
        "creation_time": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
        "state": {"type": "string"},
        "data_submitter_organizations": {"type": "list"},
        "research_organizations": {"type": "list"},
        "datasets": {"type": "list"},
        "data_submitter_organizations_invites_id": {"type": "list"},
        "research_organizations_invites_id": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    federation = get_federation(sail_portal, federation_management)

    (
        reg_new_org_response,
        reg_new_org_response_json,
    ) = sail_portal.register_new_organization(new_organization)

    pytest.new_organizations.append(
        {
            "admin_email": new_organization.admin_email,
            "admin_pass": new_organization.admin_password,
            "id": reg_new_org_response_json.get("id"),
        }
    )

    test_response = federation_management.register_data_submitter_to_data_federation(
        sail_portal, federation.get("id"), reg_new_org_response_json.get("id")
    )

    (
        new_fed_response,
        new_fed_response_json,
    ) = federation_management.get_data_federation_by_id(
        sail_portal, federation.get("id")
    )

    submitter_organizations = new_fed_response_json.get("data_submitter_organizations")
    is_added = False
    for org in submitter_organizations:
        if org.get("id") == reg_new_org_response_json.get("id"):
            is_added = True
            break

    # Assert
    is_valid = validator.validate(new_fed_response_json)
    assert_that(is_added).is_true()
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(204)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_org_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_valid_data_federation_register_invalid_data_submitter(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_org_id: str,
    request,
):
    """
    Test registering an invalid data submitter organization to a valid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_org_id: invalid organization ID
    :type invalid_org_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    federation = federations_json.get("data_federations")[
        len(federations_json.get("data_federations")) - 1
    ]

    test_response = federation_management.register_data_submitter_to_data_federation(
        sail_portal, federation.get("id"), invalid_org_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, sail_portal_target, federation_management, invalid_federation_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_invalid_data_federation_register_valid_data_submitter(
    sail_portal: SailPortalFastApi,
    sail_portal_target: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_federation_id: str,
    request,
):
    """
    Test registering a valid data submitter organization to an invalid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param sail_portal_target: Fixture
    :type sail_portal_target: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_federation_id: invalid federation ID
    :type invalid_federation_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    sail_portal_target = request.getfixturevalue(sail_portal_target)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    user_response, user_response_json = sail_portal_target.get_basic_user_info()
    target_org = user_response_json.get("organization")

    test_response = federation_management.register_data_submitter_to_data_federation(
        sail_portal, invalid_federation_id, target_org.get("id")
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_federation_id, invalid_org_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_invalid_data_federation_register_invalid_data_submitter(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_federation_id: str,
    invalid_org_id: str,
    request,
):
    """
    Test registering an invalid researcher organization to an invalid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_federation_id: invalid federation ID
    :type invalid_federation_id: str
    :param invalid_org_id: invalid organization ID
    :type invalid_org_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response = federation_management.register_data_submitter_to_data_federation(
        sail_portal, invalid_federation_id, invalid_org_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


# TODO: Revisit when [BOARD-2199] is resolved.
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal, federation_management",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
    ],
)
def test_fastapi_valid_organization_get_all_invites_authorized_user(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    request,
):
    """
    Test getting all federation invites for an organization by an authorized user.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "invites": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    _, info_response_json = sail_portal.get_basic_user_info()
    org_id = info_response_json.get("organization").get("id")

    test_response = federation_management.get_all_data_federation_organization_invites(
        sail_portal, org_id
    )

    print_response_values("Get All Data Federations", test_response, test_response)

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, sail_portal_target, federation_management",
    [
        (
            "data_owner_sail_fast_api_portal",
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
        (
            "researcher_sail_fast_api_portal",
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
    ],
)
def test_fastapi_valid_organization_get_all_invites_unauthorized_user(
    sail_portal: SailPortalFastApi,
    sail_portal_target: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    request,
):
    """
    Test getting all federation invites for an organization by an unauthorized user.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param sail_portal_target: Fixture
    :type sail_portal_target: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    sail_portal_target = request.getfixturevalue(sail_portal_target)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "detail": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, info_response_json = sail_portal_target.get_basic_user_info()
    org_id = info_response_json.get("organization").get("id")

    test_response = federation_management.get_all_data_federation_organization_invites(
        sail_portal, org_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(401)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_org_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_invalid_organization_get_all_invites(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_org_id: str,
    request,
):
    """
    Test getting all federation invites for an invalid organization.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_org_id: invalid organization ID
    :type invalid_org_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response = federation_management.get_all_data_federation_organization_invites(
        sail_portal, invalid_org_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, new_organization",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "create_valid_organization",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "create_valid_organization",
        ),
    ],
)
def test_fastapi_valid_data_federation_invite_valid_researcher(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    new_organization: Organization,
    request,
):
    """
    Test inviting a valid researcher organization to a valid federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param new_organization: new organization
    :type new_organization: Organization
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    new_organization = request.getfixturevalue(new_organization)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "data_format": {"type": "string"},
        "id": {"type": "string"},
        "creation_time": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
        "state": {"type": "string"},
        "data_submitter_organizations": {"type": "list"},
        "research_organizations": {"type": "list"},
        "datasets": {"type": "list"},
        "data_submitter_organizations_invites_id": {"type": "list"},
        "research_organizations_invites_id": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    federation = get_federation(sail_portal, federation_management)

    old_research_invite_count = len(federation.get("research_organizations_invites_id"))

    (
        reg_new_org_response,
        reg_new_org_response_json,
    ) = sail_portal.register_new_organization(new_organization)

    pytest.new_organizations.append(
        {
            "admin_email": new_organization.admin_email,
            "admin_pass": new_organization.admin_password,
            "id": reg_new_org_response_json.get("id"),
        }
    )

    test_response = federation_management.invite_researcher_to_data_federation(
        sail_portal, federation.get("id"), reg_new_org_response_json.get("id")
    )

    (
        new_fed_response,
        new_fed_response_json,
    ) = federation_management.get_data_federation_by_id(
        sail_portal, federation.get("id")
    )

    research_organizations = new_fed_response_json.get(
        "research_organizations_invites_id"
    )

    is_added = False
    if len(research_organizations) > old_research_invite_count:
        is_added = True

    # Assert
    is_valid = validator.validate(new_fed_response_json)
    assert_that(is_added).is_true()
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(204)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_org_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_valid_data_federation_invite_invalid_researcher(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_org_id: str,
    request,
):
    """
    Tests inviting an invalid research organization to a valid federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_org_id: invalid organization ID
    :type invalid_org_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    federation = get_federation(sail_portal, federation_management)

    old_research_invite_count = len(federation.get("research_organizations_invites_id"))

    test_response = federation_management.invite_researcher_to_data_federation(
        sail_portal, federation.get("id"), invalid_org_id
    )

    (
        new_fed_response,
        new_fed_response_json,
    ) = federation_management.get_data_federation_by_id(
        sail_portal, federation.get("id")
    )

    research_organizations = new_fed_response_json.get(
        "research_organizations_invites_id"
    )

    is_added = False
    if len(research_organizations) > old_research_invite_count:
        is_added = True

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_added).is_false()
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, sail_portal_target, federation_management, invalid_fed_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_invalid_data_federation_invite_valid_researcher(
    sail_portal: SailPortalFastApi,
    sail_portal_target: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_fed_id: str,
    request,
):
    """
    Tests inviting a valid researcher organization to an invalid federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param sail_portal_target: Fixture
    :type sail_portal_target: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_fed_id: invalid federation ID
    :type invalid_fed_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    sail_portal_target = request.getfixturevalue(sail_portal_target)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    target_response, target_response_json = sail_portal_target.get_basic_user_info()
    target_org = target_response_json.get("organization")

    test_response = federation_management.invite_researcher_to_data_federation(
        sail_portal, invalid_fed_id, target_org.get("id")
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_fed_id, invalid_org_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_invalid_data_federation_invite_invalid_researcher(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_fed_id: str,
    invalid_org_id: str,
    request,
):
    """
    Tests inviting an invalid researcher organization to an invalid federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_fed_id: invalid federation ID
    :type invalid_fed_id: str
    :param invalid_org_id: invalid organization ID
    :type invalid_org_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response = federation_management.invite_researcher_to_data_federation(
        sail_portal, invalid_fed_id, invalid_org_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, new_organization",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "create_valid_organization",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "create_valid_organization",
        ),
    ],
)
def test_fastapi_valid_data_federation_invite_valid_data_submitter(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    new_organization: Organization,
    request,
):
    """
    Tests inviting a valid data submitter organization to a valid federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param new_organization: Fixture
    :type new_organization: Organization
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    new_organization = request.getfixturevalue(new_organization)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "data_format": {"type": "string"},
        "id": {"type": "string"},
        "creation_time": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
        "state": {"type": "string"},
        "data_submitter_organizations": {"type": "list"},
        "research_organizations": {"type": "list"},
        "datasets": {"type": "list"},
        "data_submitter_organizations_invites_id": {"type": "list"},
        "research_organizations_invites_id": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    federation = get_federation(sail_portal, federation_management)

    old_research_invite_count = len(
        federation.get("data_submitter_organizations_invites_id")
    )

    (
        reg_new_org_response,
        reg_new_org_response_json,
    ) = sail_portal.register_new_organization(new_organization)

    pytest.new_organizations.append(
        {
            "admin_email": new_organization.admin_email,
            "admin_pass": new_organization.admin_password,
            "id": reg_new_org_response_json.get("id"),
        }
    )

    test_response = federation_management.invite_data_submitter_to_data_federation(
        sail_portal, federation.get("id"), reg_new_org_response_json.get("id")
    )

    (
        new_fed_response,
        new_fed_response_json,
    ) = federation_management.get_data_federation_by_id(
        sail_portal, federation.get("id")
    )

    research_organizations = new_fed_response_json.get(
        "data_submitter_organizations_invites_id"
    )

    if len(research_organizations) > old_research_invite_count:
        is_added = True

    # Assert
    is_valid = validator.validate(new_fed_response_json)
    assert_that(is_added).is_true()
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(204)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_org_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_valid_data_federation_invite_invalid_data_submitter(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_org_id: str,
    request,
):
    """
    Tests inviting an invalid data submitter organization to a valid federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_org_id: invalid organization ID
    :type invalid_org_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    federation = get_federation(sail_portal, federation_management)

    old_research_invite_count = len(federation.get("research_organizations_invites_id"))

    test_response = federation_management.invite_data_submitter_to_data_federation(
        sail_portal, federation.get("id"), invalid_org_id
    )

    (
        new_fed_response,
        new_fed_response_json,
    ) = federation_management.get_data_federation_by_id(
        sail_portal, federation.get("id")
    )

    research_organizations = new_fed_response_json.get(
        "research_organizations_invites_id"
    )

    is_added = False
    if len(research_organizations) > old_research_invite_count:
        is_added = True

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_added).is_false()
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, sail_portal_target, federation_management, invalid_fed_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_invalid_data_federation_invite_valid_data_submitter(
    sail_portal: SailPortalFastApi,
    sail_portal_target: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_fed_id: str,
    request,
):
    """
    Tests inviting a valid data submitter organization to an invalid federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param sail_portal_target: Fixture
    :type sail_portal_target: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_fed_id: invalid federation ID
    :type invalid_fed_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    sail_portal_target = request.getfixturevalue(sail_portal_target)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    target_response, target_response_json = sail_portal_target.get_basic_user_info()
    target_org = target_response_json.get("organization")

    test_response = federation_management.invite_data_submitter_to_data_federation(
        sail_portal, invalid_fed_id, target_org.get("id")
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_fed_id, invalid_org_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_invalid_data_federation_invite_invalid_data_submitter(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_fed_id: str,
    invalid_org_id: str,
    request,
):
    """
    Tests inviting an invalid data submitter organization to an invalid federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_fed_id: invalid federation iD
    :type invalid_fed_id: str
    :param invalid_org_id: invalid organization ID
    :type invalid_org_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response = federation_management.invite_data_submitter_to_data_federation(
        sail_portal, invalid_fed_id, invalid_org_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


# ? TODO: test_fastapi_valid_organization_get_valid_invite

# ? TODO: test_fastapi_valid_organization_get_invalid_invite

# ? TODO: test_fastapi_invalid_organization_get_valid_invite

# ? TODO: test_fastapi_invalid_organization_get_invalid_invite

# TODO: test_fastapi_valid_organization_accept_valid_invite

# TODO: test_fastapi_valid_organization_reject_valid_invite

# TODO: test_fastapi_valid_organization_accept_invalid_invite

# TODO: test_fastapi_invalid_organization_accept_valid_invite

# TODO: test_fastapi_invalid_organization_accept_invalid_invite


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, dataset_management, new_dataset",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
    ],
)
def test_fastapi_valid_data_federation_add_valid_dataset(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    request,
):
    """
    Test registering a valid dataset to a valid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param dataset_management: Fixture
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset: new dataset
    :type new_dataset: Dataset
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "data_format": {"type": "string"},
        "id": {"type": "string"},
        "creation_time": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
        "state": {"type": "string"},
        "data_submitter_organizations": {"type": "list"},
        "research_organizations": {"type": "list"},
        "datasets": {"type": "list"},
        "data_submitter_organizations_invites_id": {"type": "list"},
        "research_organizations_invites_id": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    federation = federations_json.get("data_federations")[0]

    _, new_dataset_response_json = dataset_management.register_dataset(
        sail_portal, new_dataset
    )

    pytest.new_datasets.append(
        {
            "admin_email": sail_portal.email,
            "admin_pass": sail_portal.password,
            "id": new_dataset_response_json.get("id"),
        }
    )

    # Get dataset
    _, dataset_json = dataset_management.get_dataset_by_id(
        sail_portal, new_dataset_response_json.get("id")
    )

    test_response = federation_management.add_dataset_to_federation(
        sail_portal, federation.get("id"), dataset_json.get("id")
    )

    _, updated_federation_json = federation_management.get_data_federation_by_id(
        sail_portal, federation.get("id")
    )

    updated_dataset_list = updated_federation_json.get("datasets")

    is_added = False
    for dataset in updated_dataset_list:
        if dataset.get("id") == new_dataset_response_json.get("id"):
            is_added = True
            break

    # Assert
    assert_that(is_added).is_true()
    is_valid = validator.validate(updated_federation_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(204)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, dataset_management, invalid_dataset_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_valid_data_federation_add_invalid_dataset(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    dataset_management: DataSetManagementFastApi,
    invalid_dataset_id: str,
    request,
):
    """
    Test registering an invalid dataset to a valid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param dataset_management: Fixture
    :type dataset_management: DataSetManagementFastApi
    :param invalid_dataset_id: invalid dataset ID
    :type invalid_dataset_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    dataset_management = request.getfixturevalue(dataset_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    federation = federations_json.get("data_federations")[0]

    test_response = federation_management.add_dataset_to_federation(
        sail_portal, federation.get("id"), invalid_dataset_id
    )

    _, updated_federation_json = federation_management.get_data_federation_by_id(
        sail_portal, federation.get("id")
    )

    updated_dataset_list = updated_federation_json.get("datasets")

    is_added = False
    for dataset in updated_dataset_list:
        if dataset.get("id") == invalid_dataset_id:
            is_added = True
            break

    # Assert
    assert_that(is_added).is_false()
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, dataset_management, new_dataset, invalid_federation_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_invalid_data_federation_add_valid_dataset(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    invalid_federation_id: str,
    request,
):
    """
    Test registering a valid dataset to an invalid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param dataset_management: Fixture
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset: new dataset
    :type new_dataset: Dataset
    :param invalid_federation_id: invalid federation ID
    :type invalid_federation_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, datasets_json = dataset_management.get_all_datasets(sail_portal)
    dataset = datasets_json.get("datasets")[0]

    test_response = federation_management.add_dataset_to_federation(
        sail_portal, invalid_federation_id, dataset.get("id")
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, dataset_management, invalid_dataset_id, invalid_federation_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_invalid_data_federation_add_invalid_dataset(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    dataset_management: DataSetManagementFastApi,
    invalid_dataset_id: str,
    invalid_federation_id: str,
    request,
):
    """
    Test registering an invalid dataset to an invalid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param dataset_management: Fixture
    :type dataset_management: DataSetManagementFastApi
    :param invalid_dataset_id: invalid dataset ID
    :type invalid_dataset_id: str
    :param invalid_federation_id: invalid federation ID
    :type invalid_federation_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    dataset_management = request.getfixturevalue(dataset_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, datasets_json = dataset_management.get_all_datasets(sail_portal)
    dataset = datasets_json.get("datasets")[0]

    test_response = federation_management.add_dataset_to_federation(
        sail_portal, invalid_federation_id, invalid_dataset_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


# TODO: Currently returns "Error 404: {detail: unauthorized}"
@pytest.mark.broken
@pytest.mark.parametrize(
    "sail_portal, federation_management, dataset_management, new_dataset",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
    ],
)
def test_fastapi_valid_data_federation_delete_valid_dataset(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    request,
):
    """
    Tests deleting a valid dataset from a valid federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param dataset_management: Fixture
    :type dataset_management: DataSetManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "data_format": {"type": "string"},
        "id": {"type": "string"},
        "creation_time": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
        "state": {"type": "string"},
        "data_submitter_organizations": {"type": "list"},
        "research_organizations": {"type": "list"},
        "datasets": {"type": "list"},
        "data_submitter_organizations_invites_id": {"type": "list"},
        "research_organizations_invites_id": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    federation = federations_json.get("data_federations")[0]

    (
        new_dataset_response,
        new_dataset_response_json,
    ) = dataset_management.register_dataset(sail_portal, new_dataset)
    print_response_values(
        "Register New Dataset", new_dataset_response, new_dataset_response_json
    )

    add_dataset_response = federation_management.add_dataset_to_federation(
        sail_portal, federation.get("id"), new_dataset_response_json.get("id")
    )

    print_response_values("Add Dataset", add_dataset_response, "No JSON")

    _, original_federation_json = federation_management.get_data_federation_by_id(
        sail_portal, federation.get("id")
    )
    original_datasets = original_federation_json.get("datasets")

    test_response = federation_management.remove_dataset_from_data_federation(
        sail_portal, federation.get("id"), new_dataset_response_json.get("id")
    )

    print_response_values("Test Response", test_response, test_response.json())

    # verify less datasets
    _, updated_federation_json = federation_management.get_data_federation_by_id(
        sail_portal, federation.get("id")
    )
    updated_datasets = updated_federation_json.get("datasets")

    print_federation_data(updated_federation_json)
    is_removed = False
    if len(updated_datasets) < len(original_datasets):
        is_removed = True

    for dataset in updated_datasets:
        if dataset.get("id") == new_dataset_response_json.get("id"):
            is_removed = False
            break

    # Assert
    assert_that(is_removed).is_true()
    is_valid = validator.validate(updated_federation_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(204)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_dataset_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_valid_data_federation_delete_invalid_dataset(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_dataset_id: str,
    request,
):
    """
    Tests deleting an invalid dataset from a valid federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_dataset_id: invalid dataset ID
    :type invalid_dataset_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    federation = federations_json.get("data_federations")[0]

    test_response = federation_management.remove_dataset_from_data_federation(
        sail_portal, federation.get("id"), invalid_dataset_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_fed_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_invalid_data_federation_delete_valid_dataset(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_fed_id: str,
    request,
):
    """
    Tests deleting a valid dataset from an invalid federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_fed_id: invalid federation ID
    :type invalid_fed_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    federation = federations_json.get("data_federations")[0]

    original_datasets = federation.get("datasets")
    target_dataset = original_datasets[len(original_datasets) - 1]

    test_response = federation_management.remove_dataset_from_data_federation(
        sail_portal, invalid_fed_id, target_dataset.get("id")
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_fed_id, invalid_dataset_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_invalid_data_federation_delete_invalid_dataset(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_fed_id: str,
    invalid_dataset_id: str,
    request,
):
    """
    Tests deleting an invalid dataset from an invalid federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_fed_id: invalid federation iD
    :type invalid_fed_id: str
    :param invalid_dataset_id: invalid dataset ID
    :type invalid_dataset_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response = federation_management.remove_dataset_from_data_federation(
        sail_portal, invalid_fed_id, invalid_dataset_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, dataset_management, new_dataset",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
    ],
)
def test_fastapi_federation_valid_dataset_get_existing_dataset_key(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    request,
):
    """
    Tests getting an existing dataset key from a valid dataset.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param dataset_management: Fixture
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset: Fixture
    :type new_dataset: Dataset
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {
        "dataset_key": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    federation = federations_json.get("data_federations")[0]

    _, new_dataset_response_json = dataset_management.register_dataset(
        sail_portal, new_dataset
    )

    pytest.new_datasets.append(
        {
            "admin_email": sail_portal.email,
            "admin_pass": sail_portal.password,
            "id": new_dataset_response_json.get("id"),
        }
    )

    # Get dataset
    _, dataset_json = dataset_management.get_dataset_by_id(
        sail_portal, new_dataset_response_json.get("id")
    )

    dataset_add_response = federation_management.add_dataset_to_federation(
        sail_portal, federation.get("id"), dataset_json.get("id")
    )

    (
        create_response,
        create_response_json,
    ) = federation_management.get_or_create_data_federation_dataset_key(
        sail_portal, federation.get("id"), dataset_json.get("id"), "true"
    )

    (
        test_response,
        test_response_json,
    ) = federation_management.get_existing_data_federation_dataset_key(
        sail_portal, federation.get("id"), dataset_json.get("id")
    )

    print("Get Existing", test_response, test_response_json)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(201)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, dataset_management, new_dataset",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
    ],
)
def test_fastapi_federation_valid_dataset_get_not_existing_dataset_key(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    request,
):
    """
    Tests getting a non-existing dataset key from a valid dataset.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param dataset_management: Fixture
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset: Fixture
    :type new_dataset: Dataset
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {
        "detail": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    federation = federations_json.get("data_federations")[0]

    _, new_dataset_response_json = dataset_management.register_dataset(
        sail_portal, new_dataset
    )

    pytest.new_datasets.append(
        {
            "admin_email": sail_portal.email,
            "admin_pass": sail_portal.password,
            "id": new_dataset_response_json.get("id"),
        }
    )

    # Get dataset
    _, dataset_json = dataset_management.get_dataset_by_id(
        sail_portal, new_dataset_response_json.get("id")
    )

    dataset_add_response = federation_management.add_dataset_to_federation(
        sail_portal, federation.get("id"), dataset_json.get("id")
    )

    (
        test_response,
        test_response_json,
    ) = federation_management.get_existing_data_federation_dataset_key(
        sail_portal, federation.get("id"), dataset_json.get("id")
    )

    print("Get None Existing", test_response, test_response_json)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(404)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, dataset_management, new_dataset",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
    ],
)
def test_fastapi_federation_valid_dataset_get_dataset_key(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    request,
):
    """
    Tests getting a dataset key from a valid dataset.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param dataset_management: Fixture
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset: Fixture
    :type new_dataset: Dataset
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {
        "dataset_key": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    federation = federations_json.get("data_federations")[0]

    _, new_dataset_response_json = dataset_management.register_dataset(
        sail_portal, new_dataset
    )

    pytest.new_datasets.append(
        {
            "admin_email": sail_portal.email,
            "admin_pass": sail_portal.password,
            "id": new_dataset_response_json.get("id"),
        }
    )

    # Get dataset
    _, dataset_json = dataset_management.get_dataset_by_id(
        sail_portal, new_dataset_response_json.get("id")
    )

    dataset_add_response = federation_management.add_dataset_to_federation(
        sail_portal, federation.get("id"), dataset_json.get("id")
    )

    (
        create_response,
        create_response_json,
    ) = federation_management.get_or_create_data_federation_dataset_key(
        sail_portal, federation.get("id"), dataset_json.get("id"), "true"
    )

    (
        test_response,
        test_response_json,
    ) = federation_management.get_or_create_data_federation_dataset_key(
        sail_portal, federation.get("id"), dataset_json.get("id"), "false"
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(201)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, dataset_management, new_dataset",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
    ],
)
def test_fastapi_federation_valid_dataset_get_dataset_key_create(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    request,
):
    """
    Tests getting a non-existing dataset key with "create_if_not_found' set to TRUE.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param dataset_management: Fixture
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset: Fixture
    :type new_dataset: Dataset
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {
        "dataset_key": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    federation = federations_json.get("data_federations")[0]

    _, new_dataset_response_json = dataset_management.register_dataset(
        sail_portal, new_dataset
    )

    pytest.new_datasets.append(
        {
            "admin_email": sail_portal.email,
            "admin_pass": sail_portal.password,
            "id": new_dataset_response_json.get("id"),
        }
    )

    # Get dataset
    _, dataset_json = dataset_management.get_dataset_by_id(
        sail_portal, new_dataset_response_json.get("id")
    )

    dataset_add_response = federation_management.add_dataset_to_federation(
        sail_portal, federation.get("id"), dataset_json.get("id")
    )

    (
        test_response,
        test_response_json,
    ) = federation_management.get_or_create_data_federation_dataset_key(
        sail_portal, federation.get("id"), dataset_json.get("id"), "true"
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(201)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, dataset_management, new_dataset",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
    ],
)
def test_fastapi_federation_valid_dataset_get_dataset_key_no_create(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    request,
):
    """
    Tests getting a non-existing dataset key with "create_if_not_found' set to FALSE.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param dataset_management: Fixture
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset: Fixture
    :type new_dataset: Dataset
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {
        "detail": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    federation = federations_json.get("data_federations")[0]

    _, new_dataset_response_json = dataset_management.register_dataset(
        sail_portal, new_dataset
    )

    pytest.new_datasets.append(
        {
            "admin_email": sail_portal.email,
            "admin_pass": sail_portal.password,
            "id": new_dataset_response_json.get("id"),
        }
    )

    # Get dataset
    _, dataset_json = dataset_management.get_dataset_by_id(
        sail_portal, new_dataset_response_json.get("id")
    )

    dataset_add_response = federation_management.add_dataset_to_federation(
        sail_portal, federation.get("id"), dataset_json.get("id")
    )

    (
        test_response,
        test_response_json,
    ) = federation_management.get_or_create_data_federation_dataset_key(
        sail_portal, federation.get("id"), dataset_json.get("id"), "false"
    )

    print("Get No Create", test_response, test_response_json)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(404)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, scn_size",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "Standard_D4s_v4",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "Standard_D4s_v4",
        ),
    ],
)
def test_fastapi_provision_valid_federation_valid_scn_size(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    scn_size: str,
    request,
):
    """
    Tests provisioning a valid federation with a valid scn size.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param scn_size: size of scn
    :type scn_size: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "data_federation_id": {"type": "string"},
        "secure_computation_nodes_size": {"type": "string"},
        "id": {"type": "string"},
        "creation_time": {"type": "string"},
        "organization_id": {"type": "string"},
        "smart_broker_id": {"type": "string"},
        "secure_computation_nodes_id": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    federation = get_federation(sail_portal, federation_management)

    test_response, test_response_json = federation_management.provision_data_federation(
        sail_portal, federation.get("id"), scn_size
    )

    pytest.new_provisions.append(
        {
            "admin_email": sail_portal.email,
            "admin_pass": sail_portal.password,
            "id": test_response_json.get("id"),
        }
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(201)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, scn_size",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            None,
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            None,
        ),
    ],
)
def test_fastapi_provision_valid_federation_invalid_scn_size(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    scn_size: str,
    request,
):
    """
    Tests provisioning a valid federation with an invalid scn size.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param scn_size: size of scn
    :type scn_size: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    federation = get_federation(sail_portal, federation_management)

    test_response, test_response_json = federation_management.provision_data_federation(
        sail_portal, federation.get("id"), scn_size
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_fed_id, scn_size",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            "Standard_D4s_v4",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            "Standard_D4s_v4",
        ),
    ],
)
def test_fastapi_provision_invalid_federation_valid_scn_size(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_fed_id: str,
    scn_size: str,
    request,
):
    """
    Tests provisioning an invalid federation with a valid scn size.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param scn_size: size of scn
    :type scn_size: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = federation_management.provision_data_federation(
        sail_portal, invalid_fed_id, scn_size
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_fed_id, scn_size",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            None,
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
            None,
        ),
    ],
)
def test_fastapi_provision_invalid_federation_invalid_scn_size(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_fed_id: str,
    scn_size: str,
    request,
):
    """
    Tests provisioning an invalid federation with an invalid scn size.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param scn_size: size of scn
    :type scn_size: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = federation_management.provision_data_federation(
        sail_portal, invalid_fed_id, scn_size
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
    ],
)
def test_fastapi_get_all_federation_provision_info(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    request,
):
    """
    Tests getting all federation provision info for a valid federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "data_federation_provisions": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    (
        test_response,
        test_response_json,
    ) = federation_management.get_all_data_federation_provision_info(sail_portal)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
    ],
)
def test_fastapi_get_valid_federation_provision_info(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    request,
):
    """
    Tests getting provision info for a specific valid federation by ID.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "data_federation_id": {"type": "string"},
        "secure_computation_nodes_size": {"type": "string"},
        "_id": {"type": "string"},
        "creation_time": {"type": "string"},
        "organization_id": {"type": "string"},
        "smart_broker_id": {"type": "string"},
        "secure_computation_nodes_id": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    (
        all_prov_response,
        all_prov_response_json,
    ) = federation_management.get_all_data_federation_provision_info(sail_portal)
    provisions = all_prov_response_json.get("data_federation_provisions")

    for provision in provisions:
        (
            test_response,
            test_response_json,
        ) = federation_management.get_data_federation_provision_info(
            sail_portal, provision.get("_id")
        )

        # Assert
        is_valid = validator.validate(test_response_json)
        assert_that(is_valid, description=validator.errors).is_true()
        assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_prov_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_get_invalid_federation_provision_info(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_prov_id: str,
    request,
):
    """
    Tests getting provision info for a specific valid federation by ID.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_prov_id: invalid provision ID
    :type invalid_prov_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    (
        test_response,
        test_response_json,
    ) = federation_management.get_data_federation_provision_info(
        sail_portal, invalid_prov_id
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


# TODO: Revisit after BOARD-2219 is done. (no provision state to verify deprovisioned)
@pytest.mark.broken
@pytest.mark.parametrize(
    "sail_portal, federation_management, scn_size",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "Standard_D4s_v4",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            "Standard_D4s_v4",
        ),
    ],
)
def test_fastapi_deprovision_federation_valid_provision_id(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    scn_size: str,
    request,
):
    """
    Tests deprovisioning a valid federation provision.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param scn_size: scn size
    :type scn_size: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "data_federation_id": {"type": "string"},
        "secure_computation_nodes_size": {"type": "string"},
        "id": {"type": "string"},
        "creation_time": {"type": "string"},
        "organization_id": {"type": "string"},
        "smart_broker_id": {"type": "string"},
        "secure_computation_nodes_id": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    provision = None
    for new_provision in pytest.new_provisions:
        if new_provision.get("admin_email") == sail_portal.email:
            _, provision = federation_management.get_data_federation_provision_info(
                sail_portal, new_provision.get("id")
            )
            break

    if provision is None:
        (
            _,
            provisions_json,
        ) = federation_management.get_all_data_federation_provision_info(sail_portal)
        if len(provisions_json.get("data_federation_provisions")) > 0:
            provision = provisions_json.get("data_federation_provisions")[
                len(provisions_json.get("data_federation_provisions")) - 1
            ]
        else:
            _, federations_json = federation_management.get_all_data_federations(
                sail_portal
            )
            federation = federations_json.get("data_federations")[
                len(federations_json.get("data_federations")) - 1
            ]
            _, provision = federation_management.provision_data_federation(
                sail_portal, federation.get("id"), scn_size
            )

    (
        test_response,
        test_response_json,
    ) = federation_management.deprovision_data_federation(
        sail_portal, provision.get("_id")
    )

    print_response_values(
        "Provision Data Federation", test_response, test_response_json
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(204)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_prov_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_deprovision_federation_invalid_provision_id(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_prov_id: str,
    request,
):
    """
    Tests deprovisioning a federation using an invalid provision ID.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_prov_id: invalid provision ID
    :type invalid_prov_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response = federation_management.deprovision_data_federation(
        sail_portal, invalid_prov_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
    ],
)
def test_fastapi_delete_valid_data_federation_authorized_user(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    request,
):
    """
    Test soft deleting a valid data federation by an authorized user.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "data_format": {"type": "string"},
        "id": {"type": "string"},
        "creation_time": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
        "state": {"type": "string"},
        "data_submitter_organizations": {"type": "list"},
        "research_organizations": {"type": "list"},
        "datasets": {"type": "list"},
        "data_submitter_organizations_invites_id": {"type": "list"},
        "research_organizations_invites_id": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    federation = get_federation(sail_portal, federation_management)

    test_response = federation_management.delete_data_federation_by_id(
        sail_portal, federation.get("id")
    )

    _, verify_response_json = federation_management.get_data_federation_by_id(
        sail_portal, federation.get("id")
    )

    # Assert
    is_valid = validator.validate(verify_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(verify_response_json.get("state")).is_equal_to("INACTIVE")
    assert_that(test_response.status_code).is_equal_to(204)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, sail_portal_target, federation_management",
    [
        (
            "data_owner_sail_fast_api_portal",
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
        (
            "researcher_sail_fast_api_portal",
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
        ),
    ],
)
def test_fastapi_delete_valid_data_federation_unauthorized_user(
    sail_portal: SailPortalFastApi,
    sail_portal_target: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    request,
):
    """
    Test soft deleting a valid data federation by an unauthorized user.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param sail_portal_target: Fixture
    :type sail_portal_target: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    sail_portal_target = request.getfixturevalue(sail_portal_target)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "detail": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
    federation = federations_json.get("data_federations")[
        len(federations_json.get("data_federations")) - 1
    ]

    test_response = federation_management.delete_data_federation_by_id(
        sail_portal_target, federation.get("id")
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(403)


@pytest.mark.azure
@pytest.mark.parametrize(
    "sail_portal, federation_management, invalid_federation_id",
    [
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "researcher_sail_fast_api_portal",
            "datafederation_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_delete_invalid_data_federation(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    invalid_federation_id: str,
    request,
):
    """
    Test soft deleting an invalid data federation.

    :param sail_portal: Fixture
    :type sail_portal: SailPortalFastApi
    :param federation_management: Fixture
    :type federation_management: DataFederationManagementFastApi
    :param invalid_federation_id: invalid federation ID
    :type invalid_federation_id: str
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response = federation_management.delete_data_federation_by_id(
        sail_portal, invalid_federation_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)
