# -----------------------------------------------------------
#
# Orchestrator Unit test file - Tables
#
# -----------------------------------------------------------

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
    test_response = sail.core.get_tables()
    # Assert
    assert_that(test_response).is_none()


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_list_cleared_exit_session():
    """
    Test getting a dataset list after we've exited a session
    """

    # Arrange
    logged_in_response = sail.core.get_tables()
    sail.core.exit_current_session()

    # Act
    test_response = sail.core.get_tables()

    # Assert
    assert_that(test_response).is_none()
    assert_that(test_response).is_not_equal_to(logged_in_response)


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_list_tables():
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
                    # old
                    "ColumnName": {"type": "string"},
                    # "Description": {"type": "string"},
                    "Hashtags": {"type": "string"},
                    "Name": {"type": "string"},
                    "NumberColumns": {"type": "number"},
                    "NumberRows": {"type": "number"},
                    # new
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
    }
    validator = Validator(schema)

    # Act
    test_response = sail.core.get_tables()

    # Assert

    test_response_json = json.loads(test_response)
    pretty_print(data=test_response_json)
    assert_that(test_response_json).is_not_none()

    pretty_print(data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
