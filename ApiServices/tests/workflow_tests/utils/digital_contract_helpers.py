# -------------------------------------------------------------------------------
# Engineering
# digital_contract_helpers.py
# -------------------------------------------------------------------------------
"""Digital Contract Management Helpers"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------


def get_digital_contract_payload(data_owner_guid, dataset_guid):
    """
    Helper to return template for digital contract payload

    :param data_owner_guid:
    :type data_owner_guid: str
    :param dataset_guid:
    :type dataset_guid: str
    :return: digital_contract_payload
    :rtype: dict
    """
    digital_contract_payload = {
        "DataOwnerOrganization": f"{data_owner_guid}",
        "Title": "miaw Miow phase 1",
        "Description": "The dataset will be used to train models for academic research purposes.",
        "VersionNumber": "0x0000000100000001",
        "SubscriptionDays": 28,
        "DatasetGuid": f"{{{dataset_guid}}}",
        "LegalAgreement": "The Parties acknowledge and agree that this Agreement represents the entire agreement between the Parties. In the event that the Parties desire to change, add, or otherwise modify any terms, they shall do so in writing to be signed by both parties.",
        "DatasetDRMMetadataSize": 0,
        "DatasetDRMMetadata": {},
    }
    return digital_contract_payload


def get_digital_contract_acceptance_payload(dc_guid, host_name="Data owner"):
    """
    Helper to return template for digital_contract_acceptance_payload

    :param dc_guid: digital contract guid
    :type dc_guid: str
    :param host_name: host_name, defaults to "Data owner"
    :type host_name: str, optional
    :return: digital_contract_acceptance_payload
    :rtype: dict
    """
    digital_contract_acceptance_payload = {
        "DigitalContractGuid": f"{dc_guid}",
        "Description": "The dataset will be used to train models for academic research purposes.",
        "RetentionTime": 20,
        "LegalAgreement": "The Parties acknowledge and agree that this Agreement represents the entire agreement between the Parties. In the event that the Parties desire to change, add, or otherwise modify any terms, they shall do so in writing to be signed by both parties.",
        "HostForVirtualMachines": f"{host_name}",
        "NumberOfVirtualMachines": 1,
        "HostRegion": "East US",
    }
    return digital_contract_acceptance_payload


def get_digital_contract_activate_payload(dc_guid):
    """
    Helper to return template for digital_contract_activate_payload

    :param dc_guid: digital contract guid
    :type dc_guid: str
    :return: digital_contract_activate_payload
    :rtype: dict
    """
    digital_contract_activate_payload = {
        "DigitalContractGuid": f"{dc_guid}",
        "Description": "The dataset will be used to train models for academic research purposes.",
    }
    return digital_contract_activate_payload


def get_digital_contract_associate_payload(az_template_guid, dc_guid):
    """
    Helper to return template for digital_contract_associate_payload

    :param az_template_guid: azure template guid
    :type az_template_guid: str
    :param dc_guid: digital contract guid
    :type dc_guid: str
    :return: digital_contract_associate_payload
    :rtype: dict
    """
    digital_contract_associate_payload = {
        "AzureTemplateGuid": f"{az_template_guid}",
        "ListOfDigitalContracts": [f"{dc_guid}"],
    }
    return digital_contract_associate_payload


def get_digital_contract_provision_payload(dc_guid):
    """
    Helper to return template for digital_contract_provision_payload

    :param dc_guid: digital contract guid
    :type dc_guid: str
    :return: digital_contract_provision_payload
    :rtype: dict
    """
    digital_contract_provision_payload = {
        "DigitalContractGuid": f"{dc_guid}",
        "VirtualMachineType": "Standard_D4s_v4",
    }
    return digital_contract_provision_payload
