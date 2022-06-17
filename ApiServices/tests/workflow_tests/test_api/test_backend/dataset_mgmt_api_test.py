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
from utils.dataset_helpers import get_dataset_payload
from utils.helpers import pretty_print


def debug_helper(response):
    print(f"\n----------HELLO------------")
    print(f"{response.url}")
    print(f"------------END--------------")


# TODO list_dataset - active
# TODO pull_dataset - active
# TODO register_dataset - active
# TODO delete_dataset -broken


def datasets_guids(sail_portal, dataset_management):
    """
    Helper for returning list of DatasetGuid pertaining to current eosb

    :return: list_datasets_uids
    :rtype: list
    """

    list_datasets_uids = dataset_management.list_datasets(sail_portal)[1].get("Datasets").keys()
    return list_datasets_uids


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_list_datasets(sail_portal, dataset_management, request):
    """
    Test List of Datasets

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param dataset_management: fixture, DataSetManagementApi
    :type dataset_management: .dataset_mgmt_api.DataSetManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "Datasets": {
            "type": "dict",
            "valueschema": {
                "type": "dict",
                "schema": {
                    "DataOwnerGuid": {"type": "string"},
                    "DatasetGuid": {"type": "string"},
                    "DatasetName": {"type": "string"},
                    "Description": {"type": "string"},
                    "Keywords": {"type": "string"},
                    "OrganizationName": {"type": "string"},
                    "PublishDate": {"type": "number"},
                    "Tables": {
                        "type": "dict",
                        "valueschema": {
                            "type": "dict",
                            "schema": {
                                "AllColumnProperties": {
                                    "type": "dict",
                                    "valueschema": {
                                        "type": "dict",
                                        "schema": {
                                            "ColumnIdentifier": {"type": "string"},
                                            "Description": {"type": "string"},
                                            "Tags": {"type": "string"},
                                            "Title": {"type": "string"},
                                            "Type": {"type": "string"},
                                            "Units": {"type": "string"},
                                        },
                                    },
                                },
                                "CompressedDataSizeInBytes": {"type": "number"},
                                "DataSizeInBytes": {"type": "number"},
                                "Description": {"type": "string"},
                                "NumberOfColumns": {"type": "number"},
                                "NumberOfRows": {"type": "number"},
                                "TableIdentifier": {"type": "string"},
                                "Tags": {"type": "string"},
                                "Title": {"type": "string"},
                            },
                        },
                    },
                    "VersionNumber": {"type": "string"},
                },
            },
        },
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)
    # Act
    test_response, test_response_json, user_eosb = dataset_management.list_datasets(sail_portal)
    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


# TODO run list of dataset_guid as individual tests
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_pull_dataset(sail_portal, dataset_management, request):
    """
    Test action pull of individual dataset

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param dataset_management: fixture, DataSetManagementApi
    :type dataset_management: .dataset_mgmt_api.DataSetManagementApi
    :param datasets_guids: fixture, datasets_guids
    :type datasets_guids: list of datasets guids
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "Dataset": {
            "type": "dict",
            "schema": {
                "DataOwnerGuid": {"type": "string"},
                "DatasetGuid": {"type": "string"},
                "DatasetName": {"type": "string"},
                "Description": {"type": "string"},
                "Keywords": {"type": "string"},
                "OrganizationName": {"type": "string"},
                "PublishDate": {"type": "number"},
                "Tables": {
                    "type": "dict",
                    "valueschema": {
                        "type": "dict",
                        "schema": {
                            "AllColumnProperties": {
                                "type": "dict",
                                "valueschema": {
                                    "type": "dict",
                                    "schema": {
                                        "ColumnIdentifier": {"type": "string"},
                                        "Description": {"type": "string"},
                                        "Tags": {"type": "string"},
                                        "Title": {"type": "string"},
                                        "Type": {"type": "string"},
                                        "Units": {"type": "string"},
                                    },
                                },
                            },
                            "CompressedDataSizeInBytes": {"type": "number"},
                            "DataSizeInBytes": {"type": "number"},
                            "Description": {"type": "string"},
                            "NumberOfColumns": {"type": "number"},
                            "NumberOfRows": {"type": "number"},
                            "TableIdentifier": {"type": "string"},
                            "Tags": {"type": "string"},
                            "Title": {"type": "string"},
                        },
                    },
                },
                "VersionNumber": {"type": "string"},
            },
        },
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)

    # Act
    dataset_id_tested = list()
    for uid in datasets_guids(sail_portal, dataset_management):
        print(uid)
        id_info = (test_response, test_response_json, user_eosb) = dataset_management.pull_dataset(
            sail_portal, dataset_guid=uid
        )
        dataset_id_tested.append({uid: id_info})

    # Assert
    for id in dataset_id_tested:
        for item in id.values():
            test_response = item[0]
            test_response_json = item[1]
            user_eosb = item[2]
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
def test_register_dataset(sail_portal, dataset_management, request):
    """
    Test Register dataset

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param dataset_management: fixture, DataSetManagementApi
    :type dataset_management: .dataset_mgmt_api.DataSetManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)

    # Act
    dataset_payload, _, _ = get_dataset_payload()
    test_response, test_response_json, user_eosb = dataset_management.register_dataset(
        sail_portal,
        payload=dataset_payload,
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(201)


@pytest.mark.broken
@pytest.mark.skip(reason="BOARD-314")
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_delete_dataset(sail_portal, dataset_management, request):
    """
    Blocked Board-314
    Test deleting a known dataset

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param dataset_management: fixture, DataSetManagementApi
    :type dataset_management: .dataset_mgmt_api.DataSetManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    dataset_payload, test_uuid, _ = get_dataset_payload()
    dataset_management.register_dataset(sail_portal, payload=dataset_payload)
    list_dataset_guids = list(dataset_management.list_datasets(sail_portal)[1].get("Datasets").keys())
    print(f" the uuid under test: {test_uuid}")
    test_payload = {"DatasetGuid": test_uuid}

    # Act
    # returns a 404 BOARD-314
    test_response, test_response_json, user_eosb = dataset_management.delete_dataset(sail_portal, test_payload)

    # Assert
    print(test_response)
    print(test_response_json)
    print(user_eosb)
