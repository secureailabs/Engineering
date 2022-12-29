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
from tests.workflow_tests.utils.federation_helpers import DataFederation
from tests.workflow_tests.utils.helpers import random_name


def print_response_values(function_name, response, response_json):
    print(
        f"\n\n============================================================{function_name}============================================================"
    )
    print(f"Test Response: {response}\n")
    print(f"Test Response JSON: {response_json}\n")
    print(
        f"============================================================{function_name}============================================================\n"
    )


def print_all_data(
    sail_portal: SailPortalFastApi,
    dataset_mgmt: DataSetManagementFastApi,
    federation_mgmt: DataFederationManagementFastApi,
):
    info_response, info_response_json = sail_portal.get_basic_user_info()

    org_id = info_response_json.get("organization").get("id")
    _, organization_json = sail_portal.get_organization_by_id(org_id)

    print(
        f"\n\n\n======================================================================================================================================================"
    )
    print(
        f"\t\tLogged in as: ({info_response_json.get('name')})\t\tEmail: ({info_response_json.get('email')})"
    )
    print(
        f"======================================================================================================================================================"
    )
    print(
        f"------------------------------------------------------------------------------------------------------------------------------------------------------"
    )
    print(
        f"|Organization: {organization_json.get('name')}\n\
|Description: {organization_json.get('description')}\n\
|ID: {organization_json.get('id')}\
"
    )

    _, org_users = sail_portal.get_organization_users(org_id)
    print(
        "-------------------------------------------------------------------------------------------------------------"
    )
    print(f"|Name\t\t|Email\t\t\t|Job Title\t\t|Role\t|ID")
    print(
        "-------------------------------------------------------------------------------------------------------------"
    )
    for user in org_users.get("users"):
        if user.get("job_title") == "Data Scientist":
            print(
                f"|{user.get('name')}\t|{user.get('email')}\t|{user.get('job_title')}\t\t|{user.get('role')}\t|{user.get('id')}"
            )
        else:
            print(
                f"|{user.get('name')}\t|{user.get('email')}\t|{user.get('job_title')}\t|{user.get('role')}\t|{user.get('id')}"
            )
    print(
        "-------------------------------------------------------------------------------------------------------------"
    )

    _, datasets_json = dataset_mgmt.get_all_datasets(sail_portal)
    print(
        "-------------------------------------------------------------------------------------------------------------"
    )
    print(f"\t\t| Datasets ( {organization_json.get('name')} ) |")
    print(
        "-------------------------------------------------------------------------------------------------------------"
    )
    for dataset in datasets_json.get("datasets"):
        print(
            f"|Dataset Name: {dataset.get('name')}\n\
|Description: {dataset.get('description')}\n\
|Tags: {dataset.get('tags')}\n\
|Format: {dataset.get('format')}\n\
|ID: {dataset.get('id')}\n\
|Creation Time: {dataset.get('creation_time')}\n\
|State: {dataset.get('state')}\n\
|Note: {dataset.get('state')}"
        )  # changed to 'state' for readability

        _, dataset_versions_json = dataset_mgmt.get_all_dataset_versions(
            sail_portal, dataset.get("id")
        )
        print("\t---------------------------------------------------------------------")
        print(f"\t\t\t\t| Dataset-Versions ({dataset.get('name')}) |")
        for dataset_version in dataset_versions_json.get("dataset_versions"):
            print(
                f"\t|Dataset-Version Name: {dataset_version.get('name')}\n\
    |Description: {dataset_version.get('description')}\n\
    |Dataset ID: {dataset_version.get('dataset_id')}\n\
    |ID: {dataset_version.get('id')}\n\
    |Creation Time: {dataset_version.get('dataset_version_creation_time')}\n\
    |State: {dataset.get('state')}\n\
    |Note: {dataset.get('note')}\n\n"
            )
        print(
            "-------------------------------------------------------------------------------------------------------------"
        )
    print(
        "-------------------------------------------------------------------------------------------------------------"
    )

    _, federations_json = federation_mgmt.get_all_data_federations(sail_portal)
    # federation_invites_json = federation_mgmt.get_data_federation_invites_by_organization(sail_portal, organization_json.get('id'))
    print(
        "-------------------------------------------------------------------------------------------------------------"
    )
    print(f"\t\t| Data Federations ( {organization_json.get('name')} ) |")
    print(
        "-------------------------------------------------------------------------------------------------------------"
    )
    # print(f"Invites: {federation_invites_json} ||| ")
    print(
        "-------------------------------------------------------------------------------------------------------------"
    )
    for federation in federations_json.get("data_federations"):
        data_submitter_organizations = f""
        for submitter in federation.get("data_submitter_organizations"):
            data_submitter_organizations += f"\n|\t\tName:\t{submitter.get('name')}\n|\t\tID:\t{submitter.get('id')}\n|"
        research_organizations = f""
        for researcher in federation.get("research_organizations"):
            research_organizations += f"\n|\t\t|Name:\t{researcher.get('name')}\n|\t\tID:\t{researcher.get('id')}\n|"
        dataset_list = f""
        for dataset_list_element in federation.get("datasets"):
            dataset_list += f"\n|\t\tName:\t{dataset_list_element.get('name')}\n|\t\tID:\t{dataset_list_element.get('id')}\n|"
        invite_list = f""
        for invite_list_element in federation.get("research_organizations_invites_id"):
            invite_list += f"\n|\t\tName:\t{invite_list_element.get('name')}\n|\t\tID:\t{invite_list_element.get('id')}\n|"
        print(
            f"|Federation Name:\t\t{federation.get('name')}\n\
|Description:\t\t\t{federation.get('description')}\n\
|ID:\t\t\t\t{federation.get('id')}\n\
|Data Format:\t\t\t{federation.get('data_format')}\n\
|Creation Time:\t\t\t{federation.get('creation_time')}\n\
|State:\t\t\t\t{federation.get('state')}\n\
|Data Submitter Organizations:\t{data_submitter_organizations}\n\
|Research Organizations:\t{research_organizations}\n\
|Datasets:\t\t\t{dataset_list}\n\
|Data Submitter Organizations Invites ID:\t{federation.get('data_submitter_organization_invites_id')}\n\
|Research Organizations Invites ID:\t{invite_list}"
        )
        print(
            "----------------------------------------------------------------------------------------------------"
        )


datasetfederation_payload = {
    "DataFederationDescription": "This data federation has been created for the purposes of unit testing",
    "DataFederationName": "Unit test data federation",
}

datasetfederation_payload_no_name = {
    "DataFederationDescription": "This data federation has been created for the purposes of unit testing",
}

datasetfederation_payload_no_description = {
    "DataFederationName": "Descriptionless Federation",
}

datasetfederation_payload_short_name = {
    "DataFederationDescription": "This data federation has been created for the purposes of unit testing",
    "DataFederationName": "a",
}

datasetfederation_payload_empty_name = {
    "DataFederationDescription": "This data federation has been created for the purposes of unit testing",
    "DataFederationName": "",
}

datasetfederation_payload_empty_desc = {
    "DataFederationDescription": "",
    "DataFederationName": "Unit test data federation",
}

datasetfederation_payload_empty_desc_name = {
    "DataFederationDescription": "",
    "DataFederationName": "",
}

datasetfederation_payload_long_name = {
    "DataFederationDescription": "This data federation has been created for the purposes of unit testing",
    # Our maximum name length is 255 characters
    "DataFederationName": "a" * 256,
}

datasetfederation_payload_short_desc = {
    "DataFederationDescription": "a",
    "DataFederationName": "Unit test data federation",
}

datasetfederation_payload_long_desc = {
    # Our maximum description length is 1000 characters
    "DataFederationDescription": "a" * 1001,
    "DataFederationName": "Unit test data federation",
}

datasetfederation_payload_long_desc_long_name = {
    # Our maximum description length is 1000 characters
    "DataFederationDescription": "a" * 1001,
    # Our maximum name length is 255 characters
    "DataFederationName": "a" * 256,
}


@pytest.mark.functional
@pytest.mark.parametrize(
    "data_owner_portal, researcher_portal, dataset_management, federation_management",
    [
        (
            "data_owner_sail_fast_api_portal",
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "datafederation_management_fast_api",
        ),
    ],
)
def test_debug_print_data(
    data_owner_portal: SailPortalFastApi,
    researcher_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    federation_management: DataFederationManagementFastApi,
    request,
):
    """
    Get/Print value for test debugging.

    :param data_owner_portal: _description_
    :type data_owner_portal: SailPortalFastApi
    :param researcher_portal: _description_
    :type researcher_portal: SailPortalFastApi
    :param dataset_management: _description_
    :type dataset_management: DataSetManagementFastApi
    :param federation_management: _description_
    :type federation_management: DataFederationManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    data_owner_portal = request.getfixturevalue(data_owner_portal)
    researcher_portal = request.getfixturevalue(researcher_portal)
    dataset_management = request.getfixturevalue(dataset_management)
    federation_management = request.getfixturevalue(federation_management)

    print_all_data(data_owner_portal, dataset_management, federation_management)
    print_all_data(researcher_portal, dataset_management, federation_management)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management, federation_management",
    [
        (
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "datafederation_management_fast_api",
        ),
        (
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "datafederation_management_fast_api",
        ),
    ],
)
def test_fastapi_get_all_data_federation(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    federation_management: DataFederationManagementFastApi,
    request,
):
    """
    Get all data federations associated with a dataset.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param federation_management: Fixture, DataFederationManagementFastApi
    :type federation_management: DataFederationManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "data_federations": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = federation_management.get_all_data_federations(
        sail_portal
    )

    # print_response_values("Get All Data Federations", test_response, test_response_json)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, federation_management, new_federation",
    [
        # ("data_owner_sail_fast_api_portal", "datafederation_management_fast_api", "create_valid_data_federation"),
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
    """ """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    new_federation = request.getfixturevalue(new_federation)
    new_federation.pretty_print()

    schema = {
        "id": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = federation_management.register_data_federation(
        sail_portal, new_federation
    )

    print_response_values("Register Data Federation", test_response, test_response_json)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(201)


@pytest.mark.fastapi
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
    """ """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)
    new_federation = request.getfixturevalue(new_federation)
    new_federation.pretty_print()

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


@pytest.mark.fastapi
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
    """ """
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

        print_response_values("Get Data Federation", test_response, test_response_json)

        # Assert
        is_valid = validator.validate(test_response_json)
        assert_that(is_valid, description=validator.errors).is_true()
        assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.fastapi
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
def test_fastapi_get_invalid_data_federation(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    federation_id: str,
    request,
):
    """ """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = federation_management.get_data_federation_by_id(
        sail_portal, federation_id
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.fastapi
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
    """ """
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
    _, federations_json = federation_management.get_all_data_federations(sail_portal)
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


@pytest.mark.fastapi
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
    """ """
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


@pytest.mark.fastapi
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
    """ """
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


@pytest.mark.fastapi
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
def test_fastapi_delete_valid_data_federation(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    new_name: str,
    new_description: str,
    request,
):
    """ """
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
    federation = federations_json.get("data_federations")[
        len(federations_json.get("data_federations")) - 1
    ]

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


@pytest.mark.fastapi
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
def test_fastapi_delete_invalid_data_federation(
    sail_portal: SailPortalFastApi,
    federation_management: DataFederationManagementFastApi,
    federation_id: str,
    request,
):
    """ """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response = federation_management.delete_data_federation_by_id(
        sail_portal, federation_id
    )

    # Assert
    is_valid = validator.validate(test_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


# TODO: test_fastapi_valid_data_federation_invite_valid_researcher

# TODO: test_fastapi_valid_data_federation_invite_invalid_researcher

# TODO: test_fastapi_invalid_data_federation_invite_valid_researcher

# TODO: test_fastapi_invalid_data_federation_invite_invalid_researcher

# * TODO: test_fastapi_valid_data_federation_register_valid_researcher

# * TODO: test_fastapi_valid_data_federation_register_invalid_researcher

# * TODO: test_fastapi_invalid_data_federation_register_valid_researcher

# * TODO: test_fastapi_invalid_data_federation_register_invalid_researcher

# ? TODO: test_fastapi_valid_data_federation_invite_valid_data_submitter

# ? TODO: test_fastapi_valid_data_federation_invite_invalid_data_submitter

# ? TODO: test_fastapi_invalid_data_federation_invite_valid_data_submitter

# ? TODO: test_fastapi_invalid_data_federation_invite_invalid_data_submitter

# TODO: test_fastapi_valid_data_federation_register_valid_data_submitter

# TODO: test_fastapi_valid_data_federation_register_invalid_data_submitter

# TODO: test_fastapi_invalid_data_federation_register_valid_data_submitter

# TODO: test_fastapi_invalid_data_federation_register_invalid_data_submitter


@pytest.mark.broken
@pytest.mark.parametrize(
    "sail_portal, dataset_management, federation_management",
    [
        (
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "datafederation_management_fast_api",
        ),
    ],
)
def test_fastapi_valid_organization_get_all_invites(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    federation_management: DataFederationManagementFastApi,
    request,
):
    """
    Get all data federations associated with a dataset.

    :param data_owner_portal: Fixture, SailPortalFastApi
    :type data_owner_portal: SailPortalFastApi
    :param researcher_portal: Fixture, SailPortalFastApi
    :type researcher_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param federation_management: Fixture, DataFederationManagementFastApi
    :type federation_management: DataFederationManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)
    federation_management = request.getfixturevalue(federation_management)

    schema = {
        "invites": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    _, info_response_json = sail_portal.get_basic_user_info()
    org_id = info_response_json.get("organization").get("id")

    test_response_json = (
        federation_management.get_data_federation_invites_by_organization(
            sail_portal, org_id
        )
    )

    print_response_values(
        "Get All Data Federations", test_response_json, test_response_json
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    # assert_that(test_response.status_code).is_equal_to(200)


# * TODO: test_fastapi_invalid_organization_get_all_data_federation_invites

# ? TODO: test_fastapi_valid_organization_get_valid_invite

# ? TODO: test_fastapi_valid_organization_get_invalid_invite

# ? TODO: test_fastapi_invalid_organization_get_valid_invite

# ? TODO: test_fastapi_invalid_organization_get_invalid_invite

# TODO: test_fastapi_valid_organization_accept_valid_invite

# TODO: test_fastapi_valid_organization_reject_valid_invite

# TODO: test_fastapi_valid_organization_accept_invalid_invite

# TODO: test_fastapi_invalid_organization_accept_valid_invite

# TODO: test_fastapi_invalid_organization_accept_invalid_invite

# * TODO: test_fastapi_valid_data_federation_add_valid_dataset

# * TODO: test_fastapi_valid_data_federation_add_invalid_dataset

# * TODO: test_fastapi_invalid_data_federation_add_valid_dataset

# * TODO: test_fastapi_invalid_data_federation_add_invalid_dataset

# ? TODO: test_fastapi_valid_data_federation_delete_valid_dataset

# ? TODO: test_fastapi_valid_data_federation_delete_invalid_dataset

# ? TODO: test_fastapi_invalid_data_federation_delete_valid_dataset

# ? TODO: test_fastapi_invalid_data_federation_delete_invalid_dataset

# TODO: test_fastapi_valid_data_federation_valid_dataset_get_existing_dataset_key

# TODO: test_fastapi_valid_data_federation_invalid_dataset_get_existing_dataset_key

# TODO: test_fastapi_invalid_data_federation_valid_dataset_get_existing_dataset_key

# TODO: test_fastapi_invalid_data_federation_invalid_dataset_get_existing_dataset_key

# * TODO: test_fastapi_valid_data_federation_valid_dataset_get_dataset_key

# * TODO: test_fastapi_valid_data_federation_valid_dataset_get_dataset_key_create

# * TODO: test_fastapi_valid_data_federation_valid_dataset_get_dataset_key_no_create

# * -------------------------------------------------------------- OLD API BELOW --------------------------------------------------------------
# ! -------------------------------------------------------------- OLD API BELOW --------------------------------------------------------------
# ? -------------------------------------------------------------- OLD API BELOW --------------------------------------------------------------


@pytest.mark.deprecated
def test_register_good_data_federation(
    data_owner_sail_portal, datafederation_management
):
    """
    Test Dataowner register of a good data federation

    :param data_owner_sail_portal: fixture, SailPortalApi
    :type data_owner_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datafederation_management: fixture, DataFederationManagementApi
    :type datafederation_management: datafederation_management_api.DataFederationManagementApi
    """
    # Arrange
    expect_json_schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(expect_json_schema)

    # Act
    (
        test_response,
        test_response_json,
        user_eosb,
    ) = datafederation_management.register_data_federation(
        data_owner_sail_portal, payload=datasetfederation_payload
    )

    # Assert
    assert_that(test_response.status_code).is_equal_to(201)
    # pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)


@pytest.mark.deprecated
@pytest.mark.parametrize(
    "request_information",
    [
        datasetfederation_payload_no_description,
        datasetfederation_payload_no_name,
        datasetfederation_payload_short_name,
        datasetfederation_payload_short_desc,
        datasetfederation_payload_long_name,
        datasetfederation_payload_long_desc,
        datasetfederation_payload_long_desc_long_name,
        datasetfederation_payload_empty_name,
        datasetfederation_payload_empty_desc,
        datasetfederation_payload_empty_desc_name,
    ],
)
def test_register_bad_data_federation(
    data_owner_sail_portal, datafederation_management, request_information
):
    """
    Test Dataowner register of a good data federation

    :param data_owner_sail_portal: fixture, SailPortalApi
    :type data_owner_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datafederation_management: fixture, DataFederationManagementApi
    :type datafederation_management: datafederation_management_api.DataFederationManagementApi
    """
    # Act
    test_response, _, _ = datafederation_management.register_data_federation(
        data_owner_sail_portal, payload=request_information
    )

    # Assert
    assert_that(test_response.status_code).is_equal_to(400)


@pytest.mark.deprecated
def test_list_data_federations(data_owner_sail_portal, datafederation_management):
    """
    Test Dataowner list of a data federations

    :param data_owner_sail_portal: fixture, SailPortalApi
    :type data_owner_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datafederation_management: fixture, DataFederationManagementApi
    :type datafederation_management: datafederation_management_api.DataFederationManagementApi
    """
    # Arrange
    schema = {
        "DataFederations": {
            "type": "dict",
            "valueschema": {
                "type": "dict",
                "schema": {
                    "Description": {"type": "string"},
                    "Name": {"type": "string"},
                    "DataSubmitterOrganizations": {
                        "type": "dict",
                        "keysrules": {
                            "type": "string",
                            "regex": r"{0[4567][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
                        },
                    },
                    "DatasetFamilies": {"type": "dict"},
                    "ResearcherOrganizations": {
                        "type": "dict",
                        "keysrules": {
                            "type": "string",
                            "regex": r"{0[4567][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
                        },
                    },
                    "Identifier": {
                        "type": "string",
                        "regex": r"{1[89AB][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
                    },
                    "OrganizationName": {"type": "string"},
                    "OrganizationIdentifier": {
                        "type": "string",
                        "regex": r"{0[4567][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
                    },
                },
            },
            "keysrules": {
                "type": "string",
                "regex": r"{1[89AB][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
            },
        },
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)

    # Act
    (
        test_response,
        test_response_json,
        user_eosb,
    ) = datafederation_management.list_data_federations(data_owner_sail_portal)

    # Assert
    assert_that(test_response.status_code).is_equal_to(200)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)


@pytest.mark.deprecated
def test_list_data_federations_none_linked(
    researcher_sail_portal, datafederation_management
):
    """
    Test Researcher list of a data federations who hasn't created or participated in any federation

    :param data_owner_sail_portal: fixture, SailPortalApi
    :type data_owner_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datafederation_management: fixture, DataFederationManagementApi
    :type datafederation_management: datafederation_management_api.DataFederationManagementApi
    """
    # Arrange
    schema = {
        "DataFederations": {
            "type": "dict",
            "valueschema": {
                "type": "dict",
                "schema": {
                    "Description": {"type": "string"},
                    "Name": {"type": "string"},
                    "DataSubmitterOrganizations": {
                        "type": "dict",
                        "keysrules": {
                            "type": "string",
                            "regex": r"{0[4567][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
                        },
                    },
                    "DatasetFamilies": {"type": "dict"},
                    "ResearcherOrganizations": {
                        "type": "dict",
                        "keysrules": {
                            "type": "string",
                            "regex": r"{0[4567][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
                        },
                    },
                    "Identifier": {
                        "type": "string",
                        "regex": r"{1[89AB][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
                    },
                    "OrganizationName": {"type": "string"},
                    "OrganizationIdentifier": {
                        "type": "string",
                        "regex": r"{0[4567][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
                    },
                },
            },
            "keysrules": {
                "type": "string",
                "regex": r"{1[89AB][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
            },
        },
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)

    # Act
    (
        test_response,
        test_response_json,
        user_eosb,
    ) = datafederation_management.list_data_federations(researcher_sail_portal)

    # Assert
    assert_that(test_response.status_code).is_equal_to(200)
    assert_that(user_eosb)
    federation_identifiers = test_response_json.get("DataFederations").keys()
    # We should have 0 federations that this user can use at this stage
    assert_that(len(federation_identifiers)).is_equal_to(0)
    # We still expect a well formed response with 0 entries
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
