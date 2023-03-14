# -------------------------------------------------------------------------------
# Engineering
# digital_contract_management_api_test.py
# -------------------------------------------------------------------------------
"""Digital Contract Management Api Tests"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
import time

import pytest
from api_portal.digital_contract_management_api import DigitalContractManagementApi
from api_portal.sail_portal_api import SailPortalApi
from api_portal.virtual_machine_api import VirtualMachineApi
from assertpy.assertpy import assert_that
from cerberus import Validator
from config import DATAOWNER_EMAIL, SAIL_PASS
from utils.dataset_helpers import get_dataset_payload
from utils.digital_contract_helpers import (
    get_digital_contract_acceptance_payload,
    get_digital_contract_activate_payload,
    get_digital_contract_associate_payload,
    get_digital_contract_payload,
    get_digital_contract_provision_payload,
)
from utils.helpers import pretty_print


def debug_helper(response):
    print(f"\n----------HELLO------------")
    print(f"{response.url}")
    print(f"------------END--------------")


def list_virtualmachine(sail_portal, virtualmachine_management):
    """
    Helper for return list of virtual machine guids pertaining to eosb

    :param sail_portal: fixture, sail_portal
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param virtualmachine_management: fixture, VirtualMachineApi
    :type virtualmachine_management: class  : api_portal.api_portal.virtual_machine_api.VirtualMachineApi
    :return: list_virtualmachine_guids
    :rtype: dict
    """
    vms = {}
    list_virtualmachine_dc = list(
        virtualmachine_management.list_virtual_machines(sail_portal)[1].get("VirtualMachines").keys()
    )
    for vm_dc_guid in list_virtualmachine_dc:
        vm_ip = list(
            virtualmachine_management.list_virtual_machines(sail_portal)[1]
            .get("VirtualMachines")[f"{vm_dc_guid}"]["VirtualMachinesAssociatedWithDc"]
            .keys()
        )[0]
        vms.update({f"{vm_dc_guid}": f"{vm_ip}"})
    return vms


def list_digitalcontract(sail_portal, digitalcontract_management):
    """
    Helper for yielding list of DigitalContractGuid pertaining to current eosb

    :param sail_portal: fixture, sail_portal
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param digitalcontract_management: fixture, DigitalContractManagementApi
    :type digitalcontract_management: class  : api_portal.digital_contract_management_api.DigitalContractManagementApi
    :return: list_digitalcontract_guid
    :rtype: list
    """
    list_digitalcontract_guids = (
        digitalcontract_management.list_digital_contracts(sail_portal)[1].get("DigitalContracts").keys()
    )
    return list_digitalcontract_guids


@pytest.fixture(scope="module", autouse=True)
def get_base_url(pytestconfig):
    """
    Fixture to set base_url for tests in session

    :param pytestconfig:
    :type pytestconfig:
    :return: base_url
    :rtype: string
    """
    base_url = f"https://{pytestconfig.getoption('ip')}:{pytestconfig.getoption('port')}"
    return base_url


@pytest.fixture(scope="module", autouse=True)
def setup_teardown(get_base_url):
    """
    Setup and Teardown fixture for digital contract mgmt tests

    :param get_base_url:
    :type get_base_url:
    :raises ValueError:
    :raises ValueError:
    """
    print(f"\n*******SETUP DC API TESTS*******\n")
    o_sail_portal = SailPortalApi(base_url=get_base_url, email=DATAOWNER_EMAIL, password=SAIL_PASS)
    dc_m_sail = DigitalContractManagementApi(base_url=get_base_url)
    vm_m_sail = VirtualMachineApi(base_url=get_base_url)
    yield

    print(f"\n*******TEARDOWN DC API TESTS*******\n")
    digital_contract_provisioned_payload = {"DigitalContractGuid": "{16F2A719-C772-477F-8C61-987EC3078E61}"}
    vm = list_virtualmachine(o_sail_portal, vm_m_sail)
    # Deprovision all dc in provisioned vm list
    for key in vm:
        # Update Payloads
        digital_contract_provisioned_payload.update({"DigitalContractGuid": f"{key}"})
        vm_guid_payload = {
            "VirtualMachineGuid": f"{vm[key]}",
        }
        print(f"Shutting down vm: {vm[key]}, spawned from digital contract: {key}")
        print(f"This is the vm guid: {vm_guid_payload} ")
        # Get SCN_VM state values
        vm_status = vm_m_sail.virtual_machines_status(o_sail_portal, vm_guid_payload)[1]["VirtualMachine"]["State"]
        # Wait while provisioning status is not 4, 5, 6
        while True:
            vm_status = vm_m_sail.virtual_machines_status(o_sail_portal, vm_guid_payload)[1]["VirtualMachine"]["State"]
            if vm_status == 10.0:
                raise ValueError("SCN_VM State: Provisioning Failed")
            elif vm_status == 9.0:
                raise ValueError("SCN_VM State : Delete Previously Failed")
            elif vm_status == 8.0:
                print("SCN_VM State : Deleted")
                break
            elif vm_status == 7.0:
                print("SCN_VM : Shutting Down")
                break
            elif vm_status == 6.0 or vm_status == 5.0 or vm_status == 4.0:
                # Deprovision vm in list
                output, _, _ = dc_m_sail.deprovision_digital_contract(
                    o_sail_portal, digital_contract_provisioned_payload
                )
                print(f"Response for Deprovision SCN: {output}")
                assert_that(output.status_code).is_equal_to(200)
                break
            elif vm_status == 1.0 or vm_status == 2.0:
                # Sleep for 4 min awaiting vm start and configuration
                print(f"Sleep for 4 min awaiting vm start and configuration!!!")
                time.sleep(240)
                continue


# TODO list_digitial_contracts-active
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_list_digital_contracts(digitalcontract_management, sail_portal, request):
    """
    Test List of Digital Contracts

    :param sail_portal: fixture, sail_portal
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param digitalcontract_management: fixture, DigitalContractManagementApi
    :type digitalcontract_management: class  : api_portal.digital_contract_management_api.DigitalContractManagementApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "DigitalContracts": {
            "type": "dict",
            "valueschema": {
                "type": "dict",
                "schema": {
                    "ActivationTime": {"type": "number"},
                    "AzureTemplateGuid": {"required": False, "type": "string"},
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
                    "NumberOfVirtualMachinesReady": {
                        "required": False,
                        "type": "number",
                    },
                    "ProvisioningStatus": {"type": "number"},
                    "ROName": {"type": "string"},
                    "ResearcherOrganization": {"type": "string"},
                    "RetentionTime": {"type": "number"},
                    "SubscriptionDays": {"type": "number"},
                    "Title": {"type": "string"},
                    "VersionNumber": {"type": "string"},
                },
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
    ) = digitalcontract_management.list_digital_contracts(sail_portal)

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


# TODO pull_digitial_contracts
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_pull_digital_contract(digitalcontract_management, sail_portal, request):
    """
    Test pull of Digital Contract Information

    :param sail_portal: fixture, sail_portal
    :type sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param digitalcontract_management: fixture, DigitalContractManagementApi
    :type digitalcontract_management: class  : api_portal.digital_contract_management_api.DigitalContractManagementApi
    :param request:
    :type request:
    """
    # Arrange
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "DOOName": {"type": "string"},
        "DataOwnerOrganization": {"type": "string"},
        "DigitalContract": {
            "type": "dict",
            "schema": {
                "ActivationTime": {"type": "number"},
                "AzureTemplateGuid": {"required": False, "type": "string"},
                "ContractStage": {"type": "number"},
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
                "NumberOfVirtualMachinesReady": {"required": False, "type": "number"},
                "ProvisioningStatus": {"type": "number"},
                "RetentionTime": {"type": "number"},
                "SubscriptionDays": {"type": "number"},
                "Title": {"type": "string"},
                "VersionNumber": {"type": "string"},
            },
        },
        "Eosb": {"type": "string"},
        "ROName": {"type": "string"},
        "ResearcherOrganization": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)

    # Act
    digital_contracts_id_tested = list()
    digital_contracts_list = list_digitalcontract(sail_portal, digitalcontract_management)
    for dc_guid in digital_contracts_list:
        # For each digital contract in list pull the contract information
        print(dc_guid)
        contract_info = digitalcontract_management.pull_digital_contract(sail_portal, digital_contract_guid=dc_guid)
        digital_contracts_id_tested.append({dc_guid: contract_info})

    # Assert
    for id in digital_contracts_id_tested:
        # For each digital contract information received validate response information and schema
        for item in id.values():
            test_response = item[0]
            test_response_json = item[1]
            user_eosb = item[2]
            pretty_print(msg="Test Response:", data=test_response_json)
            is_valid = validator.validate(test_response_json)
            assert_that(is_valid, description=validator.errors).is_true()
            assert_that(user_eosb)
            assert_that(test_response.status_code).is_equal_to(200)


# TODO 1 Researcher Register digitial_contract
@pytest.mark.active
def test_register_digital_contract(
    researcher_sail_portal,
    data_owner_sail_portal,
    dataset_management,
    digitalcontract_management,
):
    """
    Test Researcher can register a Digital Contract

    :param researcher_sail_portal: fixture, researcher_sail_portal
    :type researcher_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param data_owner_sail_portal: fixture, data_owner_sail_portal
    :type data_owner_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param dataset_management: .dataset_mgmt_api.DataSetManagementApi
    :type dataset_management: fixture, DataSetManagementApi
    :param digitalcontract_management: fixture, DigitalContractManagementApi
    :type digitalcontract_management: class  : api_portal.digital_contract_management_api.DigitalContractManagementApi
    """
    # Arrange
    schema = {
        "DigitalContractIdentifier": {"type": "string"},
        "Eosb": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema, require_all=True)

    # register sample dataset
    dataset_payload, test_uuid, _ = get_dataset_payload()
    dataset_management.register_dataset(
        data_owner_sail_portal,
        payload=dataset_payload,
    )
    # pull dataset information
    _, pull_response_json, _ = dataset_management.pull_dataset(
        data_owner_sail_portal,
        dataset_guid=f"{{{test_uuid}}}",
    )
    # update digital contract_payload
    data_owner_guid = pull_response_json["Dataset"]["DataOwnerGuid"]

    # Act
    # Test Researcher role Register of Digital Contract
    (test_response, test_response_json, user_eosb,) = digitalcontract_management.register_digital_contract(
        researcher_sail_portal,
        payload=get_digital_contract_payload(data_owner_guid, dataset_guid=test_uuid),
    )

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(201)


# TODO 2 Dataowner Accepts digitial_contract
@pytest.mark.active
def test_accept_digital_contract(
    researcher_sail_portal,
    data_owner_sail_portal,
    dataset_management,
    digitalcontract_management,
):
    """
    Verify Dataowner can accept Digital Contracts
    DC can only be accepted once

    :param researcher_sail_portal: fixture, researcher_sail_portal
    :type researcher_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param data_owner_sail_portal: fixture, data_owner_sail_portal
    :type data_owner_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param dataset_management: .dataset_mgmt_api.DataSetManagementApi
    :type dataset_management: fixture, DataSetManagementApi
    :param digitalcontract_management: fixture, DigitalContractManagementApi
    :type digitalcontract_management: class  : api_portal.digital_contract_management_api.DigitalContractManagementApi
    """
    # Arrange
    schema = {
        "Eosb": {"type": "string"},
        "Instructions": {"type": "string"},
        "RootEventStatus": {"type": "number"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)

    # register sample dataset
    dataset_payload, test_uuid, dataset_name = get_dataset_payload()
    dataset_management.register_dataset(
        data_owner_sail_portal,
        payload=dataset_payload,
    )
    # pull dataset information
    _, pull_response_json, _ = dataset_management.pull_dataset(
        data_owner_sail_portal,
        dataset_guid=f"{{{test_uuid}}}",
    )
    # update digital contract_payload
    data_owner_guid = pull_response_json["Dataset"]["DataOwnerGuid"]
    # Register of Digital Contract
    digitalcontract_management.register_digital_contract(
        researcher_sail_portal,
        payload=get_digital_contract_payload(data_owner_guid, dataset_guid=test_uuid),
    )
    # list all digital contracts
    list_digitalcontract_guids = list_digitalcontract(researcher_sail_portal, digitalcontract_management)
    digital_contracts_id_tested = list()
    # For each digital contract in list pull the contract information
    for dc_guid in list_digitalcontract_guids:
        print(dc_guid)
        contract_info = digitalcontract_management.pull_digital_contract(
            researcher_sail_portal, digital_contract_guid=dc_guid
        )
        digital_contracts_id_tested.append({dc_guid: contract_info})
    # Find DigitalContractGuid of new registered digital contract via DatasetName
    for id in digital_contracts_id_tested:
        for key, value in id.items():
            if dataset_name == value[1]["DigitalContract"]["DatasetName"]:
                DigitalContractGuid = key
                break
    print(f"The DigitalContractGuid associated to dataset {dataset_name} is: {DigitalContractGuid}")

    # Act
    # Test Dataowner role can accept Digital Contract
    (test_response, test_response_json, user_eosb,) = digitalcontract_management.accept_digital_contract(
        data_owner_sail_portal,
        payload=get_digital_contract_acceptance_payload(dc_guid=DigitalContractGuid),
    )

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


# TODO 3 Researcher Activate digitial_contracts
@pytest.mark.active
def test_activate_digital_contract(
    researcher_sail_portal,
    data_owner_sail_portal,
    dataset_management,
    digitalcontract_management,
):
    """
    Test Researcher can activate accepted Digital contracts

    :param researcher_sail_portal: fixture, researcher_sail_portal
    :type researcher_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param data_owner_sail_portal: fixture, data_owner_sail_portal
    :type data_owner_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param dataset_management: .dataset_mgmt_api.DataSetManagementApi
    :type dataset_management: fixture, DataSetManagementApi
    :param digitalcontract_management: fixture, DigitalContractManagementApi
    :type digitalcontract_management: class  : api_portal.digital_contract_management_api.DigitalContractManagementApi
    """
    # Arrange
    schema = {
        "Eosb": {"type": "string"},
        "Instructions": {"type": "string"},
        "RootEventStatus": {"type": "number"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)

    # register sample dataset
    dataset_payload, test_uuid, dataset_name = get_dataset_payload()
    dataset_management.register_dataset(
        data_owner_sail_portal,
        payload=dataset_payload,
    )
    # pull dataset information
    _, pull_response_json, _ = dataset_management.pull_dataset(
        data_owner_sail_portal,
        dataset_guid=f"{{{test_uuid}}}",
    )
    # update digital contract_payload
    data_owner_guid = pull_response_json["Dataset"]["DataOwnerGuid"]
    # Register of Digital Contract
    digitalcontract_management.register_digital_contract(
        researcher_sail_portal,
        payload=get_digital_contract_payload(data_owner_guid, dataset_guid=test_uuid),
    )
    # list all digital contracts
    list_digitalcontract_guids = list_digitalcontract(researcher_sail_portal, digitalcontract_management)
    digital_contracts_id_tested = list()
    # For each digital contract in list pull the contract information
    for dc_guid in list_digitalcontract_guids:
        print(dc_guid)
        contract_info = digitalcontract_management.pull_digital_contract(
            researcher_sail_portal, digital_contract_guid=dc_guid
        )
        digital_contracts_id_tested.append({dc_guid: contract_info})

    # Find DigitalContractGuid of new registered digital contract via DatasetName
    for id in digital_contracts_id_tested:
        for key, value in id.items():
            if dataset_name == value[1]["DigitalContract"]["DatasetName"]:
                DigitalContractGuid = key
                break
    print(f"The DigitalContractGuid associated to dataset {dataset_name} is: {DigitalContractGuid}")
    # Dataowner role accepts Digital Contract
    digitalcontract_management.accept_digital_contract(
        data_owner_sail_portal,
        payload=get_digital_contract_acceptance_payload(dc_guid=DigitalContractGuid),
    )

    # Act
    # Test researcher role can activate Digital Contract
    (test_response, test_response_json, user_eosb,) = digitalcontract_management.activate_digital_contract(
        researcher_sail_portal,
        payload=get_digital_contract_activate_payload(dc_guid=DigitalContractGuid),
    )

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


# TODO 4 vm hoster associate_digitial_contract_azure template
# TODO create helper function to get azure_template_payload
@pytest.mark.skip(reason="BOARD-1176, deprecated using custom templates in backend service")
@pytest.mark.active
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_associate_digital_contract(
    researcher_sail_portal,
    data_owner_sail_portal,
    sail_portal,
    dataset_management,
    digitalcontract_management,
    azuretemplate_management,
    request,
):
    """
    Test hoster of vm defined in DC can associate accepted Digital contracts

    :param researcher_sail_portal: fixture, researcher_sail_portal
    :type researcher_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param data_owner_sail_portal: fixture, data_owner_sail_portal
    :type data_owner_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param dataset_management: .dataset_mgmt_api.DataSetManagementApi
    :type dataset_management: fixture, DataSetManagementApi
    :param digitalcontract_management: fixture, DigitalContractManagementApi
    :type digitalcontract_management: class  : api_portal.digital_contract_management_api.DigitalContractManagementApi
    :param azuretemplate_management: fixture, AzureTemplateApi
    :type azuretemplate_management: class : api_portal.azure_template_managment_api.AzureTemplateApi
    """
    # Arrange
    if sail_portal == "researcher_sail_portal":
        host_name = "Researcher"
    else:
        host_name = "Data Owner"
    sail_portal = request.getfixturevalue(sail_portal)

    schema = {
        "Eosb": {"type": "string"},
        "ErrorMessage": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)
    azure_template_payload = {
        "TemplateData": {
            "Name": "Test_template",
            "Description": "Test_template_spices",
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

    # register sample dataset
    dataset_payload, test_uuid, dataset_name = get_dataset_payload()
    dataset_management.register_dataset(
        data_owner_sail_portal,
        payload=dataset_payload,
    )
    # pull dataset information
    _, pull_response_json, _ = dataset_management.pull_dataset(
        data_owner_sail_portal,
        dataset_guid=f"{{{test_uuid}}}",
    )
    # update digital contract_payload
    data_owner_guid = pull_response_json["Dataset"]["DataOwnerGuid"]
    # Register of Digital Contract
    digitalcontract_management.register_digital_contract(
        researcher_sail_portal,
        payload=get_digital_contract_payload(data_owner_guid, dataset_guid=test_uuid),
    )
    # list all digital contracts
    list_digitalcontract_guids = list_digitalcontract(researcher_sail_portal, digitalcontract_management)
    digital_contracts_id_tested = list()
    # For each digital contract in list pull the contract information
    for dc_guid in list_digitalcontract_guids:
        print(dc_guid)
        contract_info = digitalcontract_management.pull_digital_contract(
            researcher_sail_portal, digital_contract_guid=dc_guid
        )
        digital_contracts_id_tested.append({dc_guid: contract_info})
    # Find DigitalContractGuid of new registered digital contract via DatasetName
    for id in digital_contracts_id_tested:
        for key, value in id.items():
            if dataset_name == value[1]["DigitalContract"]["DatasetName"]:
                DigitalContractGuid = key
                break
    print(f"The DigitalContractGuid associated to dataset {dataset_name} is: {DigitalContractGuid}")
    # Dataowner role accepts Digital Contract
    digitalcontract_management.accept_digital_contract(
        data_owner_sail_portal,
        payload=get_digital_contract_acceptance_payload(dc_guid=DigitalContractGuid, host_name=host_name),
    )
    # Researcher activates digital contract
    digitalcontract_management.activate_digital_contract(
        researcher_sail_portal,
        payload=get_digital_contract_activate_payload(dc_guid=DigitalContractGuid),
    )
    # host of vm registers azure template
    azuretemplate_management.register_azure_template(sail_portal, payload=azure_template_payload)
    list_template_guids = list(azuretemplate_management.list_azure_templates(sail_portal)[1].get("Templates").keys())
    template_guid_under_test = list_template_guids[0]
    print(f"The TemplateGuid under test is: {template_guid_under_test}")

    # Act
    # Test host of vm role can associate Digital Contract with Azure Template
    (test_response, test_response_json, user_eosb,) = digitalcontract_management.associate_digital_contract(
        sail_portal,
        payload=get_digital_contract_associate_payload(
            az_template_guid=template_guid_under_test, dc_guid=DigitalContractGuid
        ),
    )

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


# TODO 5 Researcher provision a digital contract
# TODO new resourcegroup fails
# TODO we need to teardown after tests
@pytest.mark.functional
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_provision_digital_contract(
    researcher_sail_portal,
    data_owner_sail_portal,
    sail_portal,
    dataset_management,
    digitalcontract_management,
    # azuretemplate_management,  # Deprecated for KCA 3/11/2022
    request,
):
    """
    Test provision accepted Digital contracts,
    that have valid azure template associated.
    DC cannot be provisioned multiple times

    :param researcher_sail_portal: fixture, researcher_sail_portal
    :type researcher_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param data_owner_sail_portal: fixture, data_owner_sail_portal
    :type data_owner_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param dataset_management: .dataset_mgmt_api.DataSetManagementApi
    :type dataset_management: fixture, DataSetManagementApi
    :param digitalcontract_management: fixture, DigitalContractManagementApi
    :type digitalcontract_management: class  : api_portal.digital_contract_management_api.DigitalContractManagementApi
    :param request:
    :type request:
    """
    # Arrange
    if sail_portal == "researcher_sail_portal":
        host_name = "Researcher"
    else:
        host_name = "Data Owner"
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "Eosb": {"type": "string"},
        "Message": {"required": False, "type": "string"},
        "SecureNodeGuid": {"type": "string"},
        "Status": {"type": "number"},
    }
    validator = Validator(schema)
    # azure_template_payload = { # Deprecated for KCA 3/11/2022
    #     "TemplateData": {
    #         "Name": "Test_template",
    #         "Description": "Test_template_spices",
    #         "SubscriptionID": "3d2b9951-a0c8-4dc3-8114-2776b047b15c",
    #         "Secret": "1YEn1Y.bVTVk-dzm9voTWyf7DrgQF29xL2",
    #         "TenantID": "3e74e5ef-7e6a-4cf0-8573-680ca49b64d8",
    #         "ApplicationID": "4f909fab-ad4c-4685-b7a9-7ddaae4efb22",
    #         "ResourceGroup": "ScratchpadRg",
    #         "VirtualNetwork": "Vnet",
    #         "HostRegion": "eastus",
    #         "NetworkSecurityGroup": "NsgTemp",
    #         "VirtualMachineImage": "testing_vm",
    #     },
    # }

    # register sample dataset
    dataset_payload, test_uuid, dataset_name = get_dataset_payload()
    dataset_management.register_dataset(
        data_owner_sail_portal,
        payload=dataset_payload,
    )
    # pull dataset information
    _, pull_response_json, _ = dataset_management.pull_dataset(
        data_owner_sail_portal,
        dataset_guid=f"{{{test_uuid}}}",
    )
    # update digital contract_payload
    data_owner_guid = pull_response_json["Dataset"]["DataOwnerGuid"]
    # Register of Digital Contract
    digitalcontract_management.register_digital_contract(
        researcher_sail_portal,
        payload=get_digital_contract_payload(data_owner_guid, dataset_guid=test_uuid),
    )
    # list all digital contracts
    list_digitalcontract_guids = list_digitalcontract(researcher_sail_portal, digitalcontract_management)
    digital_contracts_id_tested = list()
    # For each digital contract in list pull the contract information
    for dc_guid in list_digitalcontract_guids:
        print(dc_guid)
        contract_info = digitalcontract_management.pull_digital_contract(
            researcher_sail_portal, digital_contract_guid=dc_guid
        )
        digital_contracts_id_tested.append({dc_guid: contract_info})
    # Find DigitalContractGuid of new registered digital contract via DatasetName
    for id in digital_contracts_id_tested:
        for key, value in id.items():
            if dataset_name == value[1]["DigitalContract"]["DatasetName"]:
                DigitalContractGuid = key
                break
    print(f"The DigitalContractGuid associated to dataset {dataset_name} is: {DigitalContractGuid}")
    # Dataowner role accepts Digital Contract
    digitalcontract_management.accept_digital_contract(
        data_owner_sail_portal,
        payload=get_digital_contract_acceptance_payload(dc_guid=DigitalContractGuid, host_name=host_name),
    )
    # Deprecated for KCA 3/11/2022
    # # host of vm role registers azure template
    # azuretemplate_management.register_azure_template(sail_portal, payload=azure_template_payload)
    # list_template_guids = list(azuretemplate_management.list_azure_templates(sail_portal)[1].get("Templates").keys())
    # template_guid_under_test = list_template_guids[0]
    # print(f"The TemplateGuid under test is: {template_guid_under_test}")
    # Researcher activates digital contract
    digitalcontract_management.activate_digital_contract(
        researcher_sail_portal,
        payload=get_digital_contract_activate_payload(dc_guid=DigitalContractGuid),
    )
    # Deprecated for KCA 3/11/2022
    # # host of vm role associates Digital Contract with Azure Template
    # digitalcontract_management.associate_digital_contract(
    #     sail_portal,
    #     payload=get_digital_contract_associate_payload(
    #         az_template_guid=template_guid_under_test, dc_guid=DigitalContractGuid
    #     ),
    # )

    # Act
    # [Researcher | Data owner]
    (test_response, test_response_json, user_eosb,) = digitalcontract_management.provision_digital_contract(
        sail_portal,
        payload=get_digital_contract_provision_payload(dc_guid=DigitalContractGuid),
    )

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)


# TODO 6 get_digital_contract_provisioning_status
@pytest.mark.skip(reason="BOARD-996")
@pytest.mark.deprecated  # Deprecated for KCA 3/11/2022, Outdated api test
@pytest.mark.parametrize(
    "sail_portal",
    [
        "researcher_sail_portal",
        "data_owner_sail_portal",
    ],
)
def test_get_dc_provision_status(
    researcher_sail_portal,
    data_owner_sail_portal,
    sail_portal,
    dataset_management,
    digitalcontract_management,
    azuretemplate_management,
    request,
):
    """
    Test get provision digital contract status api

    :param researcher_sail_portal: fixture, researcher_sail_portal
    :type researcher_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param data_owner_sail_portal: fixture, data_owner_sail_portal
    :type data_owner_sail_portal: class : api_portal.sail_portal_api.SailPortalApi
    :param dataset_management: .dataset_mgmt_api.DataSetManagementApi
    :type dataset_management: fixture, DataSetManagementApi
    :param digitalcontract_management: fixture, DigitalContractManagementApi
    :type digitalcontract_management: class  : api_portal.digital_contract_management_api.DigitalContractManagementApi
    :param azuretemplate_management: fixture, AzureTemplateApi
    :type azuretemplate_management: class : api_portal.azure_template_managment_api.AzureTemplateApi
    :param request:
    :type request:
    """
    # enum class DigitalContractProvisiongStatus # Deprecated for KCA 3/11/2022, Outdated api
    # {
    #     eProvisioning = 1,
    #     eReady = 2,
    #     eUnprovisioned = 3,
    #     eProvisioningFailed = 4
    # };
    # Arrange
    if sail_portal == "researcher_sail_portal":
        host_name = "Researcher"
    else:
        host_name = "Data Owner"
    sail_portal = request.getfixturevalue(sail_portal)
    schema = {
        "ProvisioningStatus": {"type": "number"},
        "Status": {"type": "number"},
        "VirtualMachines": {"required": False, "type": "dict"},
    }
    validator = Validator(schema)
    azure_template_payload = {
        "TemplateData": {
            "Name": "Test_template",
            "Description": "Test_template_spices",
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

    # register sample dataset
    dataset_payload, test_uuid, dataset_name = get_dataset_payload()
    dataset_management.register_dataset(
        data_owner_sail_portal,
        payload=dataset_payload,
    )
    # pull dataset information
    _, pull_response_json, _ = dataset_management.pull_dataset(
        data_owner_sail_portal,
        dataset_guid=f"{{{test_uuid}}}",
    )
    # update digital contract_payload
    data_owner_guid = pull_response_json["Dataset"]["DataOwnerGuid"]
    # Register of Digital Contract
    digitalcontract_management.register_digital_contract(
        researcher_sail_portal,
        payload=get_digital_contract_payload(data_owner_guid, dataset_guid=test_uuid),
    )
    # list all digital contracts
    list_digitalcontract_guids = list_digitalcontract(researcher_sail_portal, digitalcontract_management)
    digital_contracts_id_tested = list()
    # For each digital contract in list pull the contract information
    for dc_guid in list_digitalcontract_guids:
        print(dc_guid)
        contract_info = digitalcontract_management.pull_digital_contract(
            researcher_sail_portal, digital_contract_guid=dc_guid
        )
        digital_contracts_id_tested.append({dc_guid: contract_info})
    # Find DigitalContractGuid of new registered digital contract via DatasetName
    for id in digital_contracts_id_tested:
        for key, value in id.items():
            if dataset_name == value[1]["DigitalContract"]["DatasetName"]:
                DigitalContractGuid = key
                break
    print(f"The DigitalContractGuid associated to dataset {dataset_name} is: {DigitalContractGuid}")
    # Dataowner role accepts Digital Contract
    digitalcontract_management.accept_digital_contract(
        data_owner_sail_portal,
        payload=get_digital_contract_acceptance_payload(dc_guid=DigitalContractGuid, host_name=host_name),
    )
    # host of vm role registers azure template
    azuretemplate_management.register_azure_template(sail_portal, payload=azure_template_payload)
    list_template_guids = list(azuretemplate_management.list_azure_templates(sail_portal)[1].get("Templates").keys())
    template_guid_under_test = list_template_guids[0]
    print(f"The TemplateGuid under test is: {template_guid_under_test}")
    # Researcher activates digital contract
    digitalcontract_management.activate_digital_contract(
        researcher_sail_portal,
        payload=get_digital_contract_activate_payload(dc_guid=DigitalContractGuid),
    )
    # host of vm role associates Digital Contract with Azure Template
    digitalcontract_management.associate_digital_contract(
        sail_portal,
        payload=get_digital_contract_associate_payload(
            az_template_guid=template_guid_under_test, dc_guid=DigitalContractGuid
        ),
    )
    # [Researcher | Data owner]
    digital_contract_provision_payload = get_digital_contract_provision_payload(dc_guid=DigitalContractGuid)
    digitalcontract_management.provision_digital_contract(
        sail_portal,
        payload=digital_contract_provision_payload,
    )

    # Act
    (test_response, test_response_json, user_eosb,) = digitalcontract_management.get_provision_dc_status(
        sail_portal,
        payload=digital_contract_provision_payload,
    )

    # Assert
    pretty_print(msg="Test Response:", data=test_response_json)
    is_valid = validator.validate(test_response_json)
    assert_that(is_valid, description=validator.errors).is_true()
    assert_that(user_eosb)
    assert_that(test_response.status_code).is_equal_to(200)
