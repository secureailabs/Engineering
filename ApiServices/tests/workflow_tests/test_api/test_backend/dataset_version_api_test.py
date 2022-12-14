# -------------------------------------------------------------------------------
# Engineering
# dataset_management_api_test.py
# -------------------------------------------------------------------------------
"""Data Set Management Api Tests"""
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
from tests.workflow_tests.api_portal.dataset_management_api import \
    DataSetManagementFastApi
from tests.workflow_tests.api_portal.sail_portal_api import SailPortalFastApi
from tests.workflow_tests.utils.dataset_helpers import (DatasetVersion,
                                                        random_name)


def print_response_values(
    function_name, sail_portal: SailPortalFastApi, response, response_json, isJson
):
    print(
        f"\n\n=========={function_name}({sail_portal.email} , {sail_portal.password})=========="
    )
    print(f"Test Response: {response}\n")
    if isJson:
        for dataset in response_json.get("datasets"):
            print("\n===============================")
            print(f"Dataset ID: {dataset.get('dataset_id')}")
            print(f"Description: {dataset.get('description')}")
            print(f"Dataset Name: {dataset.get('name')}")
            print(f"Dataset Version ID: {dataset.get('id')}\n")
            organization = dataset.get("organization")
            print(f"Organization: {organization.get('name')}")
            print(f"Organization ID: {organization.get('id')}")
    else:
        print(f"Test Response JSON: {response_json}\n")


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management",
    [
        ("researcher_sail_fast_api_portal", "dataset_management_fast_api"),
        ("data_owner_sail_fast_api_portal", "dataset_management_fast_api"),
    ],
)
def test_fastapi_get_all_dataset_versions(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    request,
):
    """
    Test getting a list of dataset-versions associated with an organization.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)

    schema = {
        "dataset_versions": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    dataset_response, dataset_response_json = dataset_management.get_all_datasets(
        sail_portal
    )
    for dataset in dataset_response_json.get("datasets"):
        test_response, test_response_json = dataset_management.get_all_dataset_versions(
            sail_portal, dataset.get("id")
        )

        # Assert
        is_valid = validator.validate(test_response_json)
        assert_that(is_valid, description=validator.errors).is_true()
        assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management",
    [
        ("researcher_sail_fast_api_portal", "dataset_management_fast_api"),
        ("data_owner_sail_fast_api_portal", "dataset_management_fast_api"),
    ],
)
def test_fastapi_get_valid_dataset_version(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    request,
):
    """
    Test getting a valid dataset-versions associated with an organization.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)

    schema = {
        "dataset_id": {"type": "string"},
        "description": {"type": "string"},
        "name": {"type": "string"},
        "id": {"type": "string"},
        "dataset_version_created_time": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
        "state": {"type": "string"},
        "note": {
            "type": "string",
            "default": "NOTE",  # note variable currently None.
        },
    }

    validator = Validator(schema)

    # Act
    dataset_response, dataset_response_json = dataset_management.get_all_datasets(
        sail_portal
    )
    for dataset in dataset_response_json.get("datasets"):
        test_response, test_response_json = dataset_management.get_all_dataset_versions(
            sail_portal, dataset.get("id")
        )

        for version in test_response_json.get("dataset_versions"):
            (
                verify_response,
                verify_response_json,
            ) = dataset_management.get_dataset_version_by_id(
                sail_portal, version.get("id")
            )

            # Assert
            is_valid = validator.validate(verify_response_json)
            assert_that(is_valid, description=validator.errors).is_true()
            assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management, dataset_version_id",
    [
        (
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_get_invalid_dataset_version(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    dataset_version_id: str,
    request,
):
    """
    Test getting a list of dataset-versions associated with an organization.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param dataset_version_id: dataset version ID
    :type dataset_version_id: string
    :param request:
    :type request:
    """

    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = dataset_management.get_dataset_version_by_id(
        sail_portal, dataset_version_id
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management, new_dataset_version",
    [
        (
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_version",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_version",
        ),
    ],
)
def test_fastapi_register_valid_dataset_version(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset_version: DatasetVersion,
    request,
):
    """
    Test registering a new valid dataset-version associated with an organization.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset_version: Fixture, DatasetVersion
    :type new_dataset_version: DatasetVersion
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset_version = request.getfixturevalue(new_dataset_version)

    schema = {
        "id": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    dataset_response, dataset_response_json = dataset_management.get_all_datasets(
        sail_portal
    )

    for dataset in dataset_response_json.get("datasets"):
        if dataset.get("id") is not None:
            new_dataset_version.set_dataset_id(dataset.get("id"))
            break

    (
        register_response,
        register_response_json,
    ) = dataset_management.register_dataset_version(sail_portal, new_dataset_version)

    # Assert
    is_valid = validator.validate(register_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(register_response.status_code).is_equal_to(201)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management, new_dataset_version",
    [
        (
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_invalid_dataset_version",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_invalid_dataset_version",
        ),
    ],
)
def test_fastapi_register_invalid_dataset_version(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset_version: DatasetVersion,
    request,
):
    """
    Test registering a new invalid dataset-version associated with an organization.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset_version: Fixture, DatasetVersion
    :type new_dataset_version: DatasetVersion
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset_version = request.getfixturevalue(new_dataset_version)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    (
        register_response,
        register_response_json,
    ) = dataset_management.register_dataset_version(sail_portal, new_dataset_version)

    # Assert
    is_valid = validator.validate(register_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(register_response.status_code).is_equal_to(422)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management, new_dataset_version",
    [
        (
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_version",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_version",
        ),
    ],
)
def test_fastapi_update_valid_dataset_version_valid_credentials(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset_version: DatasetVersion,
    request,
):
    """
    Test updating a valid dataset version using valid credentials.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset_version: Fixture, DatasetVersion
    :type new_dataset_version: DatasetVersion
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset_version = request.getfixturevalue(new_dataset_version)

    schema = {
        "dataset_id": {"type": "string"},
        "description": {"type": "string"},
        "name": {"type": "string"},
        "id": {"type": "string"},
        "dataset_version_created_time": {"type": "string"},
        "organization": {
            "type": "dict",
            "schema": {
                "id": {"type": "string"},
                "name": {"type": "string"},
            },
        },
        "state": {"type": "string"},
        "note": {
            "type": "string",
            "default": "NOTE",  # note variable currently None.
        },
    }

    validator = Validator(schema)

    # Act
    dataset_response, dataset_response_json = dataset_management.get_all_datasets(
        sail_portal
    )
    for dataset in dataset_response_json.get("datasets"):
        if dataset.get("id") is not None:
            new_dataset_version.set_dataset_id(dataset.get("id"))
            break

    (
        original_response,
        original_response_json,
    ) = dataset_management.get_all_dataset_versions(
        sail_portal, new_dataset_version.dataset_id
    )

    dataset_versions = original_response_json.get("dataset_versions")
    target_dataset_version = dataset_versions[len(dataset_versions) - 1]
    original_dataset_version = DatasetVersion(
        target_dataset_version.get("dataset_id"),
        target_dataset_version.get("description"),
        target_dataset_version.get("name"),
        target_dataset_version.get("state"),
    )

    update_response = dataset_management.update_dataset_version(
        sail_portal, target_dataset_version.get("id"), new_dataset_version
    )

    (
        verify_response,
        verify_response_json,
    ) = dataset_management.get_dataset_version_by_id(
        sail_portal, target_dataset_version.get("id")
    )

    # Assert
    is_valid = validator.validate(verify_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(update_response.status_code).is_equal_to(204)
    assert_that(verify_response_json["description"]).is_equal_to(
        new_dataset_version.description
    )
    assert_that(verify_response_json["state"]).is_equal_to(new_dataset_version.state)

    # Replace values to original for consecutive tests
    update_revert_response = dataset_management.update_dataset_version(
        sail_portal, target_dataset_version.get("id"), original_dataset_version
    )


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, sail_portal_target, dataset_management, new_dataset_version",
    [
        (
            "researcher_sail_fast_api_portal",
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_version",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_version",
        ),
    ],
)
def test_fastapi_update_valid_dataset_version_invalid_credentials(
    sail_portal: SailPortalFastApi,
    sail_portal_target: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset_version: DatasetVersion,
    request,
):
    """
    Test updating a valid dataset version using invalid credentials.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param sail_portal_target: Fixture, SailPortalFastApi
    :type sail_portal_target: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset_version: Fixture, DatasetVersion
    :type new_dataset_version: DatasetVersion
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    sail_portal_target = request.getfixturevalue(sail_portal_target)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset_version = request.getfixturevalue(new_dataset_version)

    schema = {
        "detail": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    dataset_response, dataset_response_json = dataset_management.get_all_datasets(
        sail_portal_target
    )
    for dataset in dataset_response_json.get("datasets"):
        if dataset.get("id") is not None:
            new_dataset_version.set_dataset_id(dataset.get("id"))
            break

    (
        original_response,
        original_response_json,
    ) = dataset_management.get_all_dataset_versions(
        sail_portal_target, new_dataset_version.dataset_id
    )

    dataset_versions = original_response_json.get("dataset_versions")
    target_dataset_version = dataset_versions[len(dataset_versions) - 1]

    update_response = dataset_management.update_dataset_version(
        sail_portal, target_dataset_version.get("id"), new_dataset_version
    )

    # Assert
    is_valid = validator.validate(update_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(update_response.status_code).is_equal_to(404)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management, new_dataset_version, dataset_version_id",
    [
        (
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_version",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_version",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_update_invalid_dataset_version(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset_version: DatasetVersion,
    dataset_version_id: str,
    request,
):
    """
    Test updating an invalid dataset version using valid credentials.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset_version: Fixture, DatasetVersion
    :type new_dataset_version: DatasetVersion
    :param dataset_version_id: dataset version ID
    :type dataset_version_id: string
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset_version = request.getfixturevalue(new_dataset_version)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    update_response = dataset_management.update_dataset_version(
        sail_portal, dataset_version_id, new_dataset_version
    )

    # Assert
    is_valid = validator.validate(update_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(update_response.status_code).is_equal_to(422)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management",
    [
        ("researcher_sail_fast_api_portal", "dataset_management_fast_api"),
        ("data_owner_sail_fast_api_portal", "dataset_management_fast_api"),
    ],
)
def test_fastapi_delete_valid_dataset_version(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    request,
):
    """
    Test soft deleting a valid dataset version.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)

    # Act
    target_dataset_id = None
    dataset_response, dataset_response_json = dataset_management.get_all_datasets(
        sail_portal
    )
    for dataset in dataset_response_json.get("datasets"):
        if dataset.get("id") is not None:
            target_dataset_id = dataset.get("id")
            break

    (
        original_response,
        original_response_json,
    ) = dataset_management.get_all_dataset_versions(sail_portal, target_dataset_id)
    original_dataset_versions = original_response_json.get("dataset_versions")
    target_dataset_version = original_dataset_versions[
        len(original_dataset_versions) - 1
    ]

    delete_response = dataset_management.delete_dataset_version_by_id(
        sail_portal, target_dataset_version.get("id")
    )

    (
        target_dataset_version_response,
        target_dataset_version_response_json,
    ) = dataset_management.get_dataset_version_by_id(
        sail_portal, target_dataset_version.get("id")
    )

    # Assert
    assert_that(target_dataset_version_response.status_code).is_equal_to(200)
    assert_that(target_dataset_version_response_json.get("state")).is_equal_to(
        "INACTIVE"
    )
    assert_that(delete_response.status_code).is_equal_to(204)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management, dataset_version_id",
    [
        (
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_delete_invalid_dataset_version(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    dataset_version_id: str,
    request,
):
    """
    Test deleting a dataset version using an invalid dataset version ID.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param dataset_version_id: dataset version ID
    :type dataset_version_id: string
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    delete_response = dataset_management.delete_dataset_version_by_id(
        sail_portal, dataset_version_id
    )

    # Assert
    is_valid = validator.validate(delete_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(delete_response.status_code).is_equal_to(422)
