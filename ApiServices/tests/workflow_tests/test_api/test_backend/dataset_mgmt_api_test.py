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
from tests.workflow_tests.api_portal.dataset_management_api import (
    DataSetManagementFastApi,
)
from tests.workflow_tests.api_portal.sail_portal_api import SailPortalFastApi
from tests.workflow_tests.utils.dataset_helpers import Dataset, random_name


def debug_helper(response):
    print(f"\n----------HELLO------------")
    print(f"{response.url}")
    print(f"------------END--------------")


def datasets_guids(sail_portal, dataset_management):
    """
    Helper for returning list of DatasetGuid pertaining to current eosb

    :return: list_datasets_uids
    :rtype: list
    """

    list_datasets_uids = (
        dataset_management.list_datasets(sail_portal)[1].get("Datasets").keys()
    )
    return list_datasets_uids


def print_response_values(function_name, response, response_json):
    print(f"\n\n=========={function_name}==========")
    print(f"Test Response: {response}\n")
    print(f"Test Response JSON: {response_json}\n")


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management",
    [
        ("researcher_sail_fast_api_portal", "dataset_management_fast_api"),
        ("data_owner_sail_fast_api_portal", "dataset_management_fast_api"),
    ],
)
def test_fastapi_get_all_datasets(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    request,
):
    """
    Test getting a list of datasets associated with an organization.

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
        "datasets": {"type": "list"},
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = dataset_management.get_all_datasets(sail_portal)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management, new_dataset",
    [
        (
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_csv",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_csv",
        ),
    ],
)
def test_fastapi_register_valid_dataset(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    request,
):
    """
    Test registering a valid dataset.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset: new dataset
    :type new_dataset: Dataset
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {"id": {"type": "string"}}
    validator = Validator(schema)

    # Act
    test_response, test_response_json = dataset_management.register_dataset(
        sail_portal, payload=new_dataset
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(201)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management, new_dataset",
    [
        (
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_invalid_dataset",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_invalid_dataset",
        ),
    ],
)
def test_fastapi_register_invalid_dataset(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    request,
):
    """
    Test registering an invalid dataset.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset: new dataset
    :type new_dataset: Dataset
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {"error": {"type": "string"}}
    validator = Validator(schema)

    # Act
    test_response, test_response_json = dataset_management.register_dataset(
        sail_portal, payload=new_dataset
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management",
    [
        ("researcher_sail_fast_api_portal", "dataset_management_fast_api"),
        ("data_owner_sail_fast_api_portal", "dataset_management_fast_api"),
    ],
)
def test_fastapi_get_valid_dataset(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    request,
):
    """
    Test getting a valid dataset associated with an organization.

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
        "name": {"type": "string"},
        "description": {"type": "string"},
        "tags": {"type": "string"},
        "format": {"type": "string"},
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
        "note": {
            "type": "string",
            "default": "NOTE",  # note variable currently None.
        },
    }

    validator = Validator(schema)

    # Act
    test_response, test_response_json = dataset_management.get_all_datasets(sail_portal)

    # Assert
    for dataset in test_response_json.get("datasets"):
        verify_response, verify_response_json = dataset_management.get_dataset_by_id(
            sail_portal, dataset.get("id")
        )
        is_valid = validator.validate(verify_response_json)
        assert_that(is_valid, description=validator.errors).is_true()
        assert_that(verify_response.status_code).is_equal_to(200)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management, dataset_id",
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
def test_fastapi_get_invalid_dataset(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    dataset_id: str,
    request,
):
    """
    Test getting an invalid dataset associated with an organization.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param dataset_id: dataset ID
    :type dataset_id: string
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
    test_response, test_response_json = dataset_management.get_dataset_by_id(
        sail_portal, dataset_id
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(422)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, sail_portal_target, dataset_management, new_dataset",
    [
        (
            "researcher_sail_fast_api_portal",
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_csv",
        ),
        (
            "researcher_sail_fast_api_portal",
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_csv",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_fhir",
        ),
    ],
)
def test_fastapi_update_valid_dataset_invalid_credentials(
    sail_portal: SailPortalFastApi,
    sail_portal_target: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    request,
):
    """
    Test updating a valid dataset using admin credentials from a different organization (unauthorized).

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param sail_portal_target: Fixture, SailPortalFastApi
    :type sail_portal_target: SailPortalFastApi
    :param dataset_management: Fixture, DatasetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset: Fixture, Dataset
    :type new_dataset: Dataset
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    sail_portal_target = request.getfixturevalue(sail_portal_target)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {
        "detail": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    original_response, original_response_json = dataset_management.get_all_datasets(
        sail_portal_target
    )
    datasets = original_response_json.get("datasets")
    target_dataset = datasets[0]

    update_response = dataset_management.update_dataset(
        sail_portal, target_dataset.get("id"), new_dataset
    )

    # Assert
    is_valid = validator.validate(update_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(update_response.status_code).is_equal_to(403)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management, new_dataset",
    [
        (
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_invalid_dataset",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_invalid_dataset",
        ),
    ],
)
def test_fastapi_update_valid_dataset_invalid_data(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    request,
):
    """
    Test updating a valid dataset with invalid data.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset: Fixture, Dataset
    :type new_dataset: Dataset
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    original_response, original_response_json = dataset_management.get_all_datasets(
        sail_portal
    )
    original_datasets = original_response_json.get("datasets")
    target_dataset = original_datasets[len(original_datasets) - 1]

    update_response = dataset_management.update_dataset(
        sail_portal, target_dataset.get("id"), new_dataset
    )

    # Assert
    is_valid = validator.validate(update_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(update_response.status_code).is_equal_to(422)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management, new_dataset, dataset_id",
    [
        (
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_csv",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_csv",
            f"{random_name(8)}-{random_name(4)}-{random_name(4)}-{random_name(12)}",
        ),
    ],
)
def test_fastapi_update_invalid_dataset(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    dataset_id: str,
    request,
):
    """
    Test updating a dataset using an invalid dataset ID.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset: Fixture, Dataset
    :type new_dataset: Dataset
    :param dataset_id: dataset ID
    :type dataset_id: string
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {
        "error": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    update_response = dataset_management.update_dataset(
        sail_portal, dataset_id, new_dataset
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
    ],
)
def test_fastapi_delete_valid_dataset(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    request,
):
    """
    Test deleting a valid organization with valid credentials

    :param get_base_url: fixture, gets base url
    :type get_base_url: string
    :param org_id: organization ID
    :type org_id: string
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "tags": {"type": "string"},
        "format": {"type": "string"},
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
        "note": {
            "type": "string",
            "default": "NOTE",  # note variable currently None.
        },
    }

    validator = Validator(schema)

    # Act
    original_response, original_response_json = dataset_management.get_all_datasets(
        sail_portal
    )
    original_datasets = original_response_json.get("datasets")
    target_dataset = original_datasets[len(original_datasets) - 1]

    delete_response = dataset_management.delete_dataset_by_id(
        sail_portal, target_dataset.get("id")
    )

    verify_response, verify_response_json = dataset_management.get_dataset_by_id(
        sail_portal, target_dataset.get("id")
    )

    # Assert
    is_valid = validator.validate(verify_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(verify_response_json.get("state")).is_equal_to("INACTIVE")
    assert_that(verify_response.status_code).is_equal_to(200)
    assert_that(delete_response.status_code).is_equal_to(204)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, sail_portal_target, dataset_management",
    [
        (
            "researcher_sail_fast_api_portal",
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
        ),
    ],
)
def test_fastapi_delete_valid_dataset_invalid_credentials(
    sail_portal: SailPortalFastApi,
    sail_portal_target: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    request,
):
    """
    Test deleting a valid dataset using invalid credentials.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param sail_portal_target: Fixture, SailPortalFastApi
    :type sail_portal_target: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    sail_portal_target = request.getfixturevalue(sail_portal_target)
    dataset_management = request.getfixturevalue(dataset_management)

    schema = {
        "detail": {"type": "string"},
    }

    validator = Validator(schema)

    # Act
    original_response, original_response_json = dataset_management.get_all_datasets(
        sail_portal_target
    )
    original_datasets = original_response_json.get("datasets")
    target_dataset = original_datasets[len(original_datasets) - 1]

    delete_response = dataset_management.delete_dataset_by_id(
        sail_portal, target_dataset.get("id")
    )

    # Assert
    is_valid = validator.validate(delete_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(delete_response.status_code).is_equal_to(403)


@pytest.mark.fastapi
@pytest.mark.parametrize(
    "sail_portal, dataset_management, dataset_id",
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
def test_fastapi_delete_invalid_dataset(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    dataset_id: str,
    request,
):
    """
    Test deleting a dataset using an invalid dataset ID.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param dataset_id: dataset ID
    :type dataset_id: string
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
    delete_response = dataset_management.delete_dataset_by_id(sail_portal, dataset_id)

    # Assert
    is_valid = validator.validate(delete_response.json())
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(delete_response.status_code).is_equal_to(422)


@pytest.mark.broken
@pytest.mark.parametrize(
    "sail_portal, dataset_management, new_dataset",
    [
        (
            "researcher_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_csv",
        ),
        (
            "data_owner_sail_fast_api_portal",
            "dataset_management_fast_api",
            "create_valid_dataset_csv",
        ),
    ],
)
def test_fastapi_update_valid_dataset_valid_credentials(
    sail_portal: SailPortalFastApi,
    dataset_management: DataSetManagementFastApi,
    new_dataset: Dataset,
    request,
):
    """
    Test updating a valid dataset with valid credentials.

    :param sail_portal: Fixture, SailPortalFastApi
    :type sail_portal: SailPortalFastApi
    :param dataset_management: Fixture, DataSetManagementFastApi
    :type dataset_management: DataSetManagementFastApi
    :param new_dataset: Fixture, Dataset
    :type new_dataset: Dataset
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_management = request.getfixturevalue(dataset_management)
    new_dataset = request.getfixturevalue(new_dataset)

    schema = {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "tags": {"type": "string"},
        "format": {"type": "string"},
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
        "note": {
            "type": "string",
            "default": "NOTE",  # note variable currently None.
        },
    }

    validator = Validator(schema)

    # Act
    original_response, original_response_json = dataset_management.get_all_datasets(
        sail_portal
    )
    datasets = original_response_json.get("datasets")
    target_dataset = datasets[len(datasets) - 1]
    original_dataset = Dataset(
        target_dataset.get("name"),
        target_dataset.get("description"),
        target_dataset.get("tags"),
        target_dataset.get("format"),
    )

    update_response = dataset_management.update_dataset(
        sail_portal, target_dataset.get("id"), new_dataset
    )

    verify_response, verify_response_json = dataset_management.get_dataset_by_id(
        sail_portal, target_dataset.get("id")
    )

    # Assert
    is_valid = validator.validate(verify_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(update_response.status_code).is_equal_to(204)
    assert_that(verify_response_json["name"]).is_equal_to(new_dataset.name)
    assert_that(verify_response_json["description"]).is_equal_to(
        new_dataset.description
    )
    assert_that(verify_response_json["tags"]).is_equal_to(new_dataset.tags)

    # Replace values to original for consecutive tests
    update_revert_response = dataset_management.update_dataset(
        sail_portal, target_dataset.get("id"), original_dataset
    )
