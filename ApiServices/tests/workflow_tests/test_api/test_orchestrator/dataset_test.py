# -------------------------------------------------------------------------------
# Engineering
# dataset_test.py
# -------------------------------------------------------------------------------
"""Orchestrator Dataset Api Tests"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
import json

import pytest
import sail.core
from assertpy.assertpy import assert_that
from cerberus import Validator
from utils.helpers import pretty_print


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_fresh_session_fixture")
def test_list_no_loaded():
    """
    Test listing datasets with no one logged in
    """
    # Act
    test_response = sail.core.get_datasets()
    # Assert
    assert_that(test_response).is_none()


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_list_cleared_exit_session():
    """
    Test getting a dataset list after we've exited a session
    """

    # Arrange
    logged_in_response = sail.core.get_datasets()
    sail.core.exit_current_session()

    # Act
    test_response = sail.core.get_datasets()

    # Assert
    assert_that(test_response).is_none()
    assert_that(test_response).is_not_equal_to(logged_in_response)


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_list_datasets():
    """
    Test getting a dataset list once we're logged in
    """
    # Arrange
    schema = {
        "return_value": {
            "type": "dict",
            "valueschema": {
                "type": "dict",
                "schema": {
                    "OrganizationName": {"type": "string"},
                    "Description": {"type": "string"},
                    "DatasetName": {"type": "string"},
                    "DatasetGuid": {"type": "string"},
                    "VersionNumber": {"type": "string"},
                    "PublishDate": {"type": "number"},
                    "Keywords": {"type": "string"},
                    "DataOwnerGuid": {"type": "string"},
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
                                # old
                                "ColumnName": {"type": "string"},
                                # "Description": {"type": "string"},
                                "Hashtags": {"type": "string", "required": False},
                                "Name": {"type": "string"},
                                "NumberColumns": {"type": "number"},
                                "NumberRows": {"type": "number"},
                                # "NumberOfRows": {"type": "number"},
                            },
                        },
                    },
                },
            },
        },
    }
    validator = Validator(schema)

    # Act
    test_response = sail.core.get_datasets()

    # Assert
    test_response_json = json.loads(test_response)
    pretty_print(data=test_response_json)

    assert_that(test_response).is_not_none()
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
