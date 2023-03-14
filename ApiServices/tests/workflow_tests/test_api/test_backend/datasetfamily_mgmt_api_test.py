# -------------------------------------------------------------------------------
# Engineering
# dataset_management_api_test.py
# -------------------------------------------------------------------------------
"""Dataset Family Management Api Tests"""
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
from utils.helpers import pretty_print

datasetfamily_payload = {
    "DatasetFamilyDescription": "This dataset family is used for unit testing",
    "DatasetFamilyTags": "SAIL, UnitTest, TDD",
    "DatasetFamilyTitle": "Unit Test Family - Create",
}
datasetfamily_pull_payload = {
    "DatasetFamilyDescription": "This dataset family is for pulling",
    "DatasetFamilyTags": "SAIL, UnitTest, TDD",
    "DatasetFamilyTitle": "Unit Test Family",
}
datasetfamily_delete_payload = {
    "DatasetFamilyDescription": "This dataset family is for deleting",
    "DatasetFamilyTags": "SAIL, UnitTest, TDD",
    "DatasetFamilyTitle": "Unit Test Family - Delete",
}
datasetfamily_modify_payload = {
    "DatasetFamilyDescription": "This dataset family is used for unit testing",
    "DatasetFamilyTags": "SAIL, UnitTest, TDD",
    "DatasetFamilyTitle": "Unit Test Family - Modify",
}


def debug_helper(response):
    print(f"\n----------HELLO------------")
    print(f"{response.url}")
    print(f"------------END--------------")


@pytest.fixture(scope="function", autouse=True)
def clear_all_datasetfamily(data_owner_sail_portal, researcher_sail_portal, datasetfamily_management):
    """
    Fixture Function to setup and teardown, clear all dataset families

    :param data_owner_sail_portal: fixture, SailPortalApi
    :type data_owner_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DataSetFamilyManagementApi
    :type datasetfamily_management: api_portal.datasetfamily_mgmt_api.DataSetFamilyManagementApi
    """
    # Setup, clear all dataset families [data owner, researcher]
    roles = [data_owner_sail_portal, researcher_sail_portal]
    for role in roles:
        _, response_json, _ = datasetfamily_management.list_dataset_families(role)
        for dataset_family_guid in response_json.get("DatasetFamilies").keys():
            datasetfamily_management.delete_dataset_family(role, dataset_family_guid)


def get_dataset_family_guid(data_owner_sail_portal, datasetfamily_management, dataset_family_guid):
    """
    Helper Function to get dataset family guid

    :param data_owner_sail_portal: SailPortalApi
    :type data_owner_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DataSetFamilyManagementApi
    :type datasetfamily_management: api_portal.datasetfamily_mgmt_api.DataSetFamilyManagementApi
    :param dataset_family_guid: dataset_family_guid
    :type dataset_family_guid: string
    :return: DatasetFamilyGuid
    :rtype: string
    """
    _, response_json, _ = datasetfamily_management.pull_dataset_family(data_owner_sail_portal, dataset_family_guid)
    return response_json.get("DatasetFamily")["DatasetFamilyGuid"]


def get_dataset_organization_guid(data_owner_sail_portal, datasetfamily_management, dataset_family_guid):
    """
    Helper Function to get dataset organization guid

    :param data_owner_sail_portal: SailPortalApi
    :type data_owner_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DataSetFamilyManagementApi
    :type datasetfamily_management: api_portal.datasetfamily_mgmt_api.DataSetFamilyManagementApi
    :param dataset_family_guid: dataset_family_guid
    :type dataset_family_guid: string
    :return: DatasetFamilyOwnerGuid
    :rtype: string
    """
    _, response_json, _ = datasetfamily_management.pull_dataset_family(data_owner_sail_portal, dataset_family_guid)
    return response_json.get("DatasetFamily")["DatasetFamilyOwnerGuid"]


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_clear_all_datasetfamilies(sail_portal, datasetfamily_management, request):
    """
    Test Clearing of all Dataset Families

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DatasetFamilyManagementApi
    :type datasetfamily_management: class  : api_portal.datasetfamily_management_api.DatasetFamilyManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "DatasetFamilies": {
            "type": "dict",
            "valueschema": {"type": "string"},
            # All Dataset family GUIDs have the leading 5 bits set to "01100" so we check for a leading 'C' character in the GUID
            "keysrules": {
                "type": "string",
                "regex": r"{C[A-Z0-9]{7}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
            },
        },
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)

    # Act
    test_response, test_response_json, user_eosb = datasetfamily_management.list_dataset_families(sail_portal)

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)
    assert_that(len(test_response_json.get("DatasetFamilies").keys())).is_equal_to(0)
    assert_that(user_eosb)


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
@pytest.mark.parametrize(
    "malformed_datasetfamily_payload",
    [
        # Missing title
        {
            "DatasetFamilyDescription": "This dataset is used for unit testing",
            "DatasetFamilyTags": "SAIL, UnitTest, TDD",
        },
        # Missing Description
        {"DatasetFamilyTitle": "UnitTest-Family", "DatasetFamilyTags": "SAIL, UnitTest, TDD"},
    ],
)
def test_register_bad_dataset_family(sail_portal, datasetfamily_management, malformed_datasetfamily_payload, request):
    """
    Test Data owner register of a Dataset Family

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DataSetFamilyManagementApi
    :type datasetfamily_management:  api_portal.datasetfamily_mgmt_api.DataSetFamilyManagementApi
    :param malformed_datasetfamily_payload: data
    :type dict: bad data for the request
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    # Act
    # Try to register with bad data, we expect to get an error back and no JSON
    test_response, test_response_json, user_eosb = datasetfamily_management.register_dataset_family(
        sail_portal,
        payload=malformed_datasetfamily_payload,
    )

    # Assert
    assert_that(test_response.status_code).is_equal_to(400)
    assert_that(test_response_json).is_none()
    assert_that(user_eosb).is_none()


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_register_good_dataset_family(sail_portal, datasetfamily_management, request):
    """
    Test Dataowner register of a good dataset family

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DataSetFamilyManagementApi
    :type datasetfamily_management: .datasetfamily_mgmt_api.DataSetFamilyManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    expect_json_schema = {
        "DatasetFamilyIdentifier": {"type": "string"},
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(expect_json_schema, require_all=True)

    # Act
    test_response, test_response_json, user_eosb = datasetfamily_management.register_dataset_family(
        sail_portal,
        payload=datasetfamily_payload,
    )
    # Assert
    assert_that(test_response.status_code).is_equal_to(201)
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)


@pytest.mark.active_m3
def test_list_dataset_families_m3(sail_portal, datasetfamily_management):
    """
    Test List of Dataset Families

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DatasetFamilyManagementApi
    :type datasetfamily_management: class  : api_portal.datasetfamily_management_api.DatasetFamilyManagementApi
    """
    # Arrange
    schema = {
        "DatasetFamilies": {
            "type": "dict",
            "valueschema": {"type": "string"},
            # All Dataset family GUIDs have the leading 5 bits set to "01100" so we check for a leading 'C' character in the GUID
            "keysrules": {
                "type": "string",
                "regex": r"{C[A-Z0-9]{7}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
            },
        },
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)
    datasetfamily_payload = {
        "DatasetFamilyDescription": "This dataset family is for pulling",
        "DatasetFamilyTags": "SAIL, UnitTest, TDD",
        "DatasetFamilyTitle": "Unit Test Family",
    }

    for x in range(2):
        datasetfamily_management.register_dataset_family(sail_portal, payload=datasetfamily_payload)

    # Act
    test_response, test_response_json, user_eosb = datasetfamily_management.list_dataset_families(sail_portal)

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)

    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)
    assert_that(len(test_response_json.get("DatasetFamilies").keys())).is_equal_to(2)


@pytest.mark.active_m5
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_list_dataset_families_m5(
    data_owner_sail_portal, researcher_sail_portal, sail_portal, datasetfamily_management, request
):
    """
    Test List of Dataset Families

    :param data_owner_sail_portal: fixture, SailPortalApi
    :type data_owner_sail_portal: api_portal.sail_portal_api.SailPortalApi
    :param researcher_sail_portal: fixture, SailPortalApi
    :type researcher_sail_portal: api_portal.sail_portal_api.SailPortalApi
    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DatasetFamilyManagementApi
    :type datasetfamily_management: class  : api_portal.datasetfamily_management_api.DatasetFamilyManagementApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "DatasetFamilies": {
            "type": "dict",
            "valueschema": {
                "type": "dict",
                "schema": {
                    "DatasetFamilyActive": {"type": "boolean"},
                    "DatasetFamilyOwnerGuid": {"type": "string"},
                    "DatasetFamilyTags": {"type": "string"},
                    "DatasetFamilyTitle": {"type": "string"},
                    "OrganizationName": {"type": "string"},
                },
            },
            # Dataset GUIDs have their leading 5 bits as: 1C, which means the first two bytes can be 1C, 1D, 1E, or 1F
            "keysrules": {
                "type": "string",
                "regex": r"{1[CDEF][A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}}",
            },
        },
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)

    portals = [data_owner_sail_portal, researcher_sail_portal]
    for portal in portals:
        datasetfamily_management.register_dataset_family(portal, payload=datasetfamily_pull_payload)

    # Act
    test_response, test_response_json, user_eosb = datasetfamily_management.list_dataset_families(sail_portal)

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)

    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)
    assert_that(len(test_response_json.get("DatasetFamilies").keys())).is_equal_to(2)


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_pulling_known_dataset_family(sail_portal, datasetfamily_management, request):
    """
    Test Pulling a known dataset family

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DatasetFamilyManagementApi
    :type datasetfamily_management: class  : api_portal.datasetfamily_management_api.DatasetFamilyManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "DatasetFamily": {
            "type": "dict",
            "schema": {
                "DatasetFamilyActive": {"type": "boolean"},
                "DatasetFamilyDescription": {"type": "string"},
                "DatasetFamilyGuid": {"type": "string"},
                "DatasetFamilyOwnerGuid": {"type": "string"},
                "DatasetFamilyTags": {"type": "string"},
                "DatasetFamilyTitle": {"type": "string"},
                "OrganizationName": {"type": "string"},
                "VersionNumber": {"type": "string"},
            },
        },
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)

    datasetfamily_management.register_dataset_family(sail_portal, payload=datasetfamily_pull_payload)
    # Now get a list of our dataset families
    list_datasetfamily_guids = list(
        datasetfamily_management.list_dataset_families(sail_portal)[1].get("DatasetFamilies").keys()
    )

    test_dataset_family_guid = list_datasetfamily_guids[0]

    # Act
    test_response, test_response_json, user_eosb = datasetfamily_management.pull_dataset_family(
        sail_portal, test_dataset_family_guid
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)
    assert_that(test_response_json.get("DatasetFamily").get("DatasetFamilyGuid")).is_equal_to(test_dataset_family_guid)
    assert_that(test_response_json.get("DatasetFamily").get("DatasetFamilyOwnerGuid")).is_equal_to(
        sail_portal.get_basic_user_info()[1].get("OrganizationGuid")
    )
    assert_that(user_eosb)


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_delete_known_dataset_family(sail_portal, datasetfamily_management, request):
    """
    Test Data owner deleting a known dataset family

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DatasetFamilyManagementApi
    :type datasetfamily_management: class  : api_portal.datasetfamily_management_api.DatasetFamilyManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)

    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)
    # Make sure we have at least one dataset in the database
    test_response = datasetfamily_management.register_dataset_family(sail_portal, payload=datasetfamily_delete_payload)

    list_datasetfamily_guids = list(
        datasetfamily_management.list_dataset_families(sail_portal)[1].get("DatasetFamilies").keys()
    )

    test_dataset_family_guid = list_datasetfamily_guids[0]

    # Act
    test_response, test_response_json, user_eosb = datasetfamily_management.delete_dataset_family(
        sail_portal, test_dataset_family_guid
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)
    assert_that(user_eosb)


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_delete_not_existing_dataset_family(sail_portal, datasetfamily_management, request):

    """
    Test Data owner deleting a guid that doesn't exist

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DatasetFamilyManagementApi
    :type datasetfamily_management: class  : api_portal.datasetfamily_management_api.DatasetFamilyManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    bad_guid = "{C123456-1234-4321-1324-ABCDEFFEDCBA}"
    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)

    # Act
    test_response, test_response_json, user_eosb = datasetfamily_management.delete_dataset_family(sail_portal, bad_guid)

    # Assert
    assert_that(test_response.status_code).is_equal_to(404)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_modify_dataset_correctly(sail_portal, datasetfamily_management, request):
    """
    Test Data owner modify of a Dataset Family

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DataSetFamilyManagementApi
    :type datasetfamily_management: .datasetfamily_mgmt_api.DataSetFamilyManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "DatasetFamily": {
            "type": "dict",
            "schema": {
                "DatasetFamilyActive": {"type": "boolean"},
                "DatasetFamilyDescription": {"type": "string"},
                "DatasetFamilyGuid": {"type": "string"},
                "DatasetFamilyOwnerGuid": {"type": "string"},
                "DatasetFamilyTags": {"type": "string"},
                "DatasetFamilyTitle": {"type": "string"},
                "OrganizationName": {"type": "string"},
                "VersionNumber": {"type": "string"},
            },
        },
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)
    # Add a known dataset
    # register sample dataset
    datasetfamily_management.register_dataset_family(
        sail_portal,
        payload=datasetfamily_modify_payload,
    )
    # Now get a list of our dataset families
    list_datasetfamily_guids = list(
        datasetfamily_management.list_dataset_families(sail_portal)[1].get("DatasetFamilies").keys()
    )
    test_dataset_family_guid = list_datasetfamily_guids[0]
    # Pull dataset family
    _, pull_response_json, _ = datasetfamily_management.pull_dataset_family(sail_portal, test_dataset_family_guid)

    dataset_family = pull_response_json.get("DatasetFamily")
    dataset_family["DatasetFamilyTitle"] = "Modified Dataset Family Title"

    datasetfamily_management.update_datset_family(sail_portal, dataset_family)

    # Act
    # Pull it again to verify the change
    test_response, test_response_json, user_eosb = datasetfamily_management.pull_dataset_family(
        sail_portal, test_dataset_family_guid
    )
    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)
    assert_that(test_response_json.get("DatasetFamily")["DatasetFamilyTitle"]).is_equal_to(
        "Modified Dataset Family Title"
    )
    assert_that(user_eosb)


@pytest.mark.active_m5
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_modify_dataset_add_tags(sail_portal, datasetfamily_management, request):
    """
    Test Data owner modify of a Dataset Family

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DataSetFamilyManagementApi
    :type datasetfamily_management: .datasetfamily_mgmt_api.DataSetFamilyManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "DatasetFamily": {
            "type": "dict",
            "schema": {
                "DatasetFamilyActive": {"type": "boolean"},
                "DatasetFamilyDescription": {"type": "string"},
                "DatasetFamilyGuid": {"type": "string"},
                "DatasetFamilyOwnerGuid": {"type": "string"},
                "DatasetFamilyTags": {"type": "string"},
                "DatasetFamilyTitle": {"type": "string"},
                "OrganizationName": {"type": "string"},
                "VersionNumber": {"type": "string"},
            },
        },
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)
    # Add a known dataset without tags
    datasetfamily_payload = {
        "DatasetFamilyDescription": "This dataset family is used for unit testing",
        "DatasetFamilyTitle": "Unit Test Family - Modify",
    }
    # register sample dataset
    datasetfamily_management.register_dataset_family(
        sail_portal,
        payload=datasetfamily_payload,
    )
    # Now get a list of our dataset families
    list_datasetfamily_guids = list(
        datasetfamily_management.list_dataset_families(sail_portal)[1].get("DatasetFamilies").keys()
    )
    test_dataset_family_guid = list_datasetfamily_guids[0]
    # Pull dataset family
    _, pull_response_json, _ = datasetfamily_management.pull_dataset_family(sail_portal, test_dataset_family_guid)

    dataset_family = pull_response_json.get("DatasetFamily")
    dataset_family["DatasetFamilyTags"] = "SAIL, UnitTest, TDD"

    datasetfamily_management.update_datset_family(sail_portal, dataset_family)

    # Act
    # Pull it again to verify the change
    test_response, test_response_json, user_eosb = datasetfamily_management.pull_dataset_family(
        sail_portal, test_dataset_family_guid
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(200)
    assert_that(test_response_json.get("DatasetFamily")["DatasetFamilyTags"]).is_equal_to("SAIL, UnitTest, TDD")
    assert_that(user_eosb)


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_modify_dataset_guid(sail_portal, datasetfamily_management, request):
    """
    Test Data owner modify of a Dataset Family's guid, not allowed

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DataSetFamilyManagementApi
    :type datasetfamily_management: .datasetfamily_mgmt_api.DataSetFamilyManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)
    # Add a known dataset
    # register sample dataset
    datasetfamily_management.register_dataset_family(
        sail_portal,
        payload=datasetfamily_modify_payload,
    )
    # Now get a list of our dataset families
    list_datasetfamily_guids = list(
        datasetfamily_management.list_dataset_families(sail_portal)[1].get("DatasetFamilies").keys()
    )

    test_dataset_family_guid = list_datasetfamily_guids[0]
    # Pull dataset family
    _, pull_response_json, _ = datasetfamily_management.pull_dataset_family(sail_portal, test_dataset_family_guid)

    dataset_family = pull_response_json.get("DatasetFamily")
    dataset_family_guid = dataset_family["DatasetFamilyGuid"]
    # Replace the object's GUID
    dataset_family["DatasetFamilyGuid"] = "{C123456-1234-4321-1324-ABCDEFFEDCBA}"

    # Act
    test_response, test_response_json, user_eosb = datasetfamily_management.update_datset_family(
        sail_portal, dataset_family
    )

    # Assert
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(test_response.status_code).is_equal_to(404)
    assert_that(user_eosb)
    # Verify dataset family guid remains unchanged
    assert_that(dataset_family_guid).is_equal_to(
        get_dataset_family_guid(sail_portal, datasetfamily_management, test_dataset_family_guid)
    )


@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_modify_dataset_organization_guid(sail_portal, datasetfamily_management, request):
    """
    Test modify of a Dataset Family's organization guid, not allowed

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param datasetfamily_management: fixture, DataSetFamilyManagementApi
    :type datasetfamily_management: .datasetfamily_mgmt_api.DataSetFamilyManagementApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {"Eosb": {"type": "string"}, "Status": {"type": "number"}}
    validator = Validator(schema)
    # Add a known dataset
    # register sample dataset
    datasetfamily_management.register_dataset_family(
        sail_portal,
        payload=datasetfamily_modify_payload,
    )
    # Pull the dataset
    # Now get a list of our dataset families
    list_datasetfamily_guids = list(
        datasetfamily_management.list_dataset_families(sail_portal)[1].get("DatasetFamilies").keys()
    )
    test_dataset_family_guid = list_datasetfamily_guids[0]
    # Pull dataset family
    _, pull_response_json, _ = datasetfamily_management.pull_dataset_family(sail_portal, test_dataset_family_guid)
    dataset_family = pull_response_json.get("DatasetFamily")
    dataset_org_guid = dataset_family["DatasetFamilyOwnerGuid"]
    # Update DatasetFamilyOwnerGuid
    dataset_family["DatasetFamilyOwnerGuid"] = "{C123456-1234-4321-1324-ABCDEFFEDCBA}"

    # Act
    test_response, test_response_json, user_eosb = datasetfamily_management.update_datset_family(
        sail_portal, dataset_family
    )

    # Assert
    assert_that(test_response.status_code).is_equal_to(404)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    # Verify dataset organization guid is unchanged
    assert_that(dataset_org_guid).is_equal_to(
        get_dataset_organization_guid(sail_portal, datasetfamily_management, test_dataset_family_guid)
    )
