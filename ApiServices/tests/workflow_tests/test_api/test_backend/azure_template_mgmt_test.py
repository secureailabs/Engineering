# -------------------------------------------------------------------------------
# Engineering
# azure_template_managment_api_test.py
# -------------------------------------------------------------------------------
"""Azure Template Api Tests"""
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
from utils.az_template_helpers import get_az_template_payload
from utils.helpers import pretty_print


def debug_helper(response):
    print(f"\n----------HELLO------------")
    print(f"{response.url}")
    print(f"------------END--------------")


@pytest.fixture(scope="function", autouse=True)
def delete_all_azure_template(data_owner_sail_portal, researcher_sail_portal, azuretemplate_management):
    """
    Helper Function to delete all azure templates

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param azuretemplate_management: fixture, AzureTemplateApi
    :type azuretemplate_management: class  : api_portal.azure_template_managment_api.AzureTemplateApi
    """
    roles = [data_owner_sail_portal, researcher_sail_portal]
    for role in roles:
        _, response_json, _ = azuretemplate_management.list_azure_templates(role)
        for template_guid in response_json.get("Templates").keys():
            payload = {"TemplateGuid": template_guid}
            del_response, _, _ = azuretemplate_management.delete_azure_template(role, payload)
            assert_that(del_response.status_code).is_equal_to(200)


# TODO Register azure template
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_register_azure_templates(sail_portal, azuretemplate_management, request):
    """
    Test Register of Azure Templates

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param azuretemplate_management: fixture, AzureTemplateApi
    :type azuretemplate_management: class  : api_portal.azure_template_managment_api.AzureTemplateApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)

    # Act
    test_response, test_response_json, user_eosb = azuretemplate_management.register_azure_template(
        sail_portal, payload=get_az_template_payload()
    )

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(201)


# TODO list azure templates
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_list_azure_templates(sail_portal, azuretemplate_management, request):
    """
    Test List of Azure Templates
    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param azuretemplate_management: fixture, AzureTemplateApi
    :type azuretemplate_management: class  : api_portal.azure_template_managment_api.AzureTemplateApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
        "Templates": {"type": "dict"},
    }
    validator = Validator(schema)
    # Register Unique Azure Templates
    azuretemplate_management.register_azure_template(sail_portal, payload=get_az_template_payload())

    # Act
    test_response, test_response_json, user_eosb = azuretemplate_management.list_azure_templates(sail_portal)

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


# TODO pull azure template
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_pull_azure_templates(sail_portal, azuretemplate_management, request):
    """
    Test Pull of Azure Template

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param azuretemplate_management: fixture, AzureTemplateApi
    :type azuretemplate_management: class  : api_portal.azure_template_managment_api.AzureTemplateApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
        "Template": {"type": "dict"},
    }
    validator = Validator(schema)
    # Register Unique Azure Templates
    azuretemplate_management.register_azure_template(sail_portal, payload=get_az_template_payload())
    list_template_guids = list(azuretemplate_management.list_azure_templates(sail_portal)[1].get("Templates").keys())
    template_guid_under_test = list_template_guids[0]
    print(f"This is full list of azure templates registered: {list_template_guids}")
    print(f"This is the template guid under test: {template_guid_under_test}")
    test_payload = template_guid_under_test

    # Act
    test_response, test_response_json, user_eosb = azuretemplate_management.pull_azure_template(
        sail_portal, test_payload
    )

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


# TODO Update azure template
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_update_azure_templates(sail_portal, azuretemplate_management, request):
    """
    Test Update of Azure Template (Name, Description)

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param azuretemplate_management: fixture, AzureTemplateApi
    :type azuretemplate_management: class  : api_portal.azure_template_managment_api.AzureTemplateApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)
    # Register Unique Azure Templates
    azuretemplate_management.register_azure_template(sail_portal, payload=get_az_template_payload())
    list_template_guids = list(azuretemplate_management.list_azure_templates(sail_portal)[1].get("Templates").keys())
    template_guid_under_test = list_template_guids[0]
    print(f"This is full list of azure templates registered: {list_template_guids}")
    print(f"This is the template guid under test: {template_guid_under_test}")
    update_payload = {
        "TemplateGuid": template_guid_under_test,
        "TemplateData": {
            "Name": "Test_template4Update",
            "Description": "Test_template_spices1",
            "SubscriptionID": "3d2b9951-a0c8-4dc3-8114-2776b047b15c",
            "Secret": "1YEn1Y.bVTVk-dzm9voTWyf7DrgQF29xL2",
            "TenantID": "3e74e5ef-7e6a-4cf0-8573-680ca49b64d8",
            "ApplicationID": "4f909fab-ad4c-4685-b7a9-7ddaae4efb22",
            "ResourceGroup": "ScratchpadRg",
            "VirtualNetwork": "Vnet",
            "HostRegion": "eastus",
            "NetworkSecurityGroup": "NsgTemp",
            "VirtualMachineImage": "testing_vm",
        },
    }

    # Act
    test_response, test_response_json, user_eosb = azuretemplate_management.update_azure_template(
        sail_portal, payload=update_payload
    )

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)
    # Verify updated values are as expected
    verify_template_json = azuretemplate_management.pull_azure_template(sail_portal, template_guid_under_test)[1].get(
        "Template"
    )
    set(update_payload.get("TemplateData").items()).issubset(set(verify_template_json.items()))


# TODO Delete azure template
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_delete_azure_templates(sail_portal, azuretemplate_management, request):
    """
    Test Delete of Azure Template

    :param sail_portal: fixture, SailPortalApi
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param azuretemplate_management: fixture, AzureTemplateApi
    :type azuretemplate_management: class  : api_portal.azure_template_managment_api.AzureTemplateApi
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)
    # Register Unique Azure Template
    azuretemplate_management.register_azure_template(sail_portal, payload=get_az_template_payload())
    # List Azure Template
    list_template_guids = list(azuretemplate_management.list_azure_templates(sail_portal)[1].get("Templates").keys())
    template_guid_under_test = list_template_guids[0]
    print(f"This is full list of azure templates registered: {list_template_guids}")
    print(f"This is the template guid under test: {template_guid_under_test}")
    test_payload = {"TemplateGuid": list_template_guids[0]}

    # Act
    test_response, test_response_json, user_eosb = azuretemplate_management.delete_azure_template(
        sail_portal, test_payload
    )

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)
    # Verify template_guid under test is not in list of azure templates
    assert template_guid_under_test not in list(
        azuretemplate_management.list_azure_templates(sail_portal)[1].get("Templates").keys()
    )
