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
import json

import pytest
from assertpy.assertpy import assert_that
from cerberus import Validator
from utils.helpers import pretty_print

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


@pytest.mark.active
def test_register_good_data_federation(data_owner_sail_portal, datafederation_management):
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
    test_response, test_response_json, user_eosb = datafederation_management.register_data_federation(
        data_owner_sail_portal, payload=datasetfederation_payload
    )

    # Assert
    assert_that(test_response.status_code).is_equal_to(201)
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)


@pytest.mark.active
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
def test_register_bad_data_federation(data_owner_sail_portal, datafederation_management, request_information):
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


@pytest.mark.active
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
    test_response, test_response_json, user_eosb = datafederation_management.list_data_federations(
        data_owner_sail_portal
    )

    # Assert
    assert_that(test_response.status_code).is_equal_to(200)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)


@pytest.mark.active
def test_list_data_federations_none_linked(researcher_sail_portal, datafederation_management):
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
    test_response, test_response_json, user_eosb = datafederation_management.list_data_federations(
        researcher_sail_portal
    )

    # Assert
    assert_that(test_response.status_code).is_equal_to(200)
    assert_that(user_eosb)
    federation_identifiers = test_response_json.get("DataFederations").keys()
    # We should have 0 federations that this user can use at this stage
    assert_that(len(federation_identifiers)).is_equal_to(0)
    # We still expect a well formed response with 0 entries
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
