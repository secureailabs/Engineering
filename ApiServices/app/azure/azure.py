# -------------------------------------------------------------------------------
# Engineering
# azure.py
# -------------------------------------------------------------------------------
"""Temporary azure functions"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
import json
import os
from ipaddress import ip_address

from pydantic import BaseModel, Field, StrictStr

from azure.core.exceptions import AzureError
from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode


class DeploymentResponse(BaseModel):
    """Deployment response."""

    status: StrictStr = Field(...)
    ip_address: StrictStr = Field(...)
    note: StrictStr = Field(...)


class DeleteResponse(BaseModel):
    """Delete response."""

    status: StrictStr = Field(...)
    note: StrictStr = Field(...)


def create_resource_group(accountCredentials, resource_group_name, location):
    """Deploy the template to a resource group."""
    client = ResourceManagementClient(accountCredentials["credentials"], accountCredentials["subscription_id"])
    response = client.resource_groups.create_or_update(resource_group_name, {"location": location})  # type: ignore
    return response.properties.provisioning_state  # type: ignore


def authenticate(client_id, client_secret, tenant_id, subscription_id):
    """Authenticate using client_id and client_secret."""
    credentials = ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    return {"credentials": credentials, "subscription_id": subscription_id}


def deploy_template(accountCredentials, resource_group_name, template, parameters):
    """Deploy the template to a resource group."""
    client = ResourceManagementClient(accountCredentials["credentials"], accountCredentials["subscription_id"])

    parameters = {k: {"value": v} for k, v in parameters.items()}
    deployment_properties = {
        "mode": DeploymentMode.incremental,
        "template": template,
        "parameters": parameters,
    }

    deployment_async_operation = client.deployments.begin_create_or_update(
        resource_group_name, "azure-sample", {"properties": deployment_properties}  # type: ignore
    )
    deployment_async_operation.wait()
    print("deployment_async_operation result ", deployment_async_operation.result())

    return deployment_async_operation.status()


def delete_resouce_group(accountCredentials, resource_group_name) -> DeleteResponse:
    """Delete the resource group."""
    try:
        client = ResourceManagementClient(accountCredentials["credentials"], accountCredentials["subscription_id"])
        delete_async_operation = client.resource_groups.begin_delete(resource_group_name)
        delete_async_operation.wait()

        return DeleteResponse(status="Success", note="")
    except AzureError as azure_error:
        print("AzureError: ", azure_error)
        return DeleteResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        print("Exception: ", exception)
        return DeleteResponse(status="Fail", note=str(exception))


def get_ip(accountCredentials, resource_group_name, ip_resource_name):
    """Get the IP address of the resource."""
    client = NetworkManagementClient(accountCredentials["credentials"], accountCredentials["subscription_id"])
    foo = client.public_ip_addresses.get(resource_group_name, ip_resource_name)
    return foo.ip_address


def deploy_module(account_credentials, deployment_name, module_name) -> DeploymentResponse:
    """Deploy the template to a resource group."""
    try:
        print("Deploying module: ", module_name)

        # Each module will be deployed in a unique resource group
        resource_group_name = deployment_name

        # Create the resource group
        create_resource_group(account_credentials, resource_group_name, "eastus")

        template_path = os.path.join(module_name + ".json")

        with open(template_path, "r") as template_file_fd:
            template = json.load(template_file_fd)

        parameters = {
            "vmName": module_name,
            "vmSize": "Standard_D4s_v4",
            "vmImageResourceId": "/subscriptions/3d2b9951-a0c8-4dc3-8114-2776b047b15c/resourceGroups/NginxImageStorageRg/providers/Microsoft.Compute/images/"
            + module_name,
            "adminUserName": "sailuser",
            "adminPassword": "SailPassword@123",
            "subnetName": "PlatformService_eastus",
            "virtualNetworkId": "/subscriptions/3d2b9951-a0c8-4dc3-8114-2776b047b15c/resourceGroups/ScratchPad_Network_RG/providers/Microsoft.Network/virtualNetworks/MGMT_Vnet",
        }
        deploy_status = deploy_template(account_credentials, resource_group_name, template, parameters)
        print(module_name + " server status: ", deploy_status)

        virtual_machine_public_ip = get_ip(account_credentials, resource_group_name, module_name + "-ip")

        return DeploymentResponse(status="Success", ip_address=virtual_machine_public_ip, note="Deployment Successful")

    except AzureError as azure_error:
        print("AzureError: ", azure_error)
        return DeploymentResponse(status="Fail", ip_address="", note=str(azure_error))
    except Exception as exception:
        print("Exception: ", exception)
        return DeploymentResponse(status="Fail", ip_address="", note=str(exception))
