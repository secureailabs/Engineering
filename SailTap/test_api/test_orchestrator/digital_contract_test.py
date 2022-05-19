# -----------------------------------------------------------
#
# Orchestrator Unit test file - Digital contracts
#
# -----------------------------------------------------------

import json

import pytest
import sail.core
from assertpy.assertpy import assert_that
from cerberus import Validator


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_fresh_session_fixture")
def test_list_no_loaded():
    """
    Test listing digital contracts with no one logged in
    """
    # Arrange

    # Act
    test_response = sail.core.get_digital_contracts()
    # Assert
    assert_that(test_response).is_none()


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_list_logged_in():
    """
    Test getting a digital contract list once we are properly logged in
    """

    schema = {
        "return_value": {
            "type": "dict",
            "valueschema": {
                "type": "dict",
                "schema": {
                    "ActivationTime": {"type": "number"},
                    "AzureTemplateGuid": {"type": "string", "required": False},
                    "ContractStage": {"type": "number"},
                    "DOOName": {"type": "string"},
                    "DataOwnerOrganization": {"type": "string"},
                    "DatasetDRMMetadata": {"type": "dict"},
                    "DatasetDRMMetadataSize": {"type": "number"},
                    "DatasetGuid": {"type": "string"},
                    "DatasetName": {"type": "string"},
                    "Description": {"type": "string"},
                    "DigitalContractGuid": {"type": "string"},
                    "Eula": {"type": "string"},
                    "EulaAcceptedByDOOAuthorizedUser": {"type": "string"},
                    "EulaAcceptedByROAuthorizedUser": {"type": "string"},
                    "ExpirationTime": {"type": "number"},
                    "HostForVirtualMachines": {"type": "string"},
                    "HostRegion": {"type": "string"},
                    "LastActivity": {"type": "number"},
                    "LegalAgreement": {"type": "string"},
                    "Note": {"type": "string"},
                    "NumberOfVirtualMachines": {"type": "number"},
                    "NumberOfVirtualMachinesReady": {"type": "number", "required": False},
                    "ProvisioningStatus": {"type": "number"},
                    "ROName": {"type": "string"},
                    "ResearcherOrganization": {"type": "string"},
                    "RetentionTime": {"type": "number"},
                    "SubscriptionDays": {"type": "number"},
                    "Title": {"type": "string"},
                    "VersionNumber": {"type": "string"},
                },
            },
            "keysrules": {
                "type": "string",
                "regex": r"{1[4567][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
            },
        },
    }
    validator = Validator(schema)

    # Act
    test_response = sail.core.get_digital_contracts()

    # Assert
    assert_that(test_response).is_not_none()
    json_response = {}
    json_response["return_value"] = json.loads(test_response)
    is_valid = validator.validate(json_response)
    assert_that(is_valid, description=validator.errors).is_true()


@pytest.mark.active
@pytest.mark.usefixtures("orchestrator_login_fixture")
def test_list_cleared_exit_session():
    """
    Test getting a digital contract list after we've exited a session
    """

    # Arrange
    logged_in_response = sail.core.get_digital_contracts()
    sail.core.exit_current_session()

    # Act
    test_response = sail.core.get_digital_contracts()

    # Assert
    assert_that(test_response).is_none()
    assert_that(test_response).is_not_equal_to(logged_in_response)
