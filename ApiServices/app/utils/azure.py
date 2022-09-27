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
import random
from datetime import datetime

from app.utils.secrets import get_secret
from pydantic import BaseModel, Field, StrictStr

from azure.core.exceptions import AzureError
from azure.identity import ClientSecretCredential

from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode
from azure.mgmt.storage import StorageManagementClient
from azure.storage.fileshare import FileSasPermissions, ShareDirectoryClient, generate_file_sas


class DeploymentResponse(BaseModel):
    """Deployment response."""

    status: StrictStr = Field(...)
    response: StrictStr = Field(default="")
    ip_address: StrictStr = Field(default="")
    note: StrictStr = Field(...)


class DeleteResponse(BaseModel):
    """Delete response."""

    status: StrictStr = Field(...)
    note: StrictStr = Field(...)


def authentication_shared_access_signature(
    account_credentials,
    account_name: str,
    resource_group_name: str,
    file_path: str,
    share_name: str,
    permission: str,
    expiry: datetime,
):
    """Get the connection string for the storage account and file share."""
    try:
        # Create a client to the storage account.
        storage_client = StorageManagementClient(
            account_credentials["credentials"], account_credentials["subscription_id"]
        )

        # Get the storage account key.
        keys = storage_client.storage_accounts.list_keys(resource_group_name, account_name)

        # Create a connection string to the file share.
        sas_token = generate_file_sas(
            account_name=account_name,
            share_name=share_name,
            file_path=[file_path],
            account_key=keys.keys[0].value,  # type: ignore
            permission=FileSasPermissions.from_string(permission),
            expiry=expiry,
        )

        return DeploymentResponse(status="Success", response=sas_token, note="Deployment Successful")
    except AzureError as azure_error:
        return DeploymentResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        return DeploymentResponse(status="Fail", note=str(exception))


def file_share_create_directory(connection_string, file_share_name, directory_name):
    """Create a directory in the file share."""
    try:
        directory_client = ShareDirectoryClient.from_connection_string(
            conn_str=connection_string, share_name=file_share_name, directory_path=directory_name
        )
        directory_client.create_directory()

        return DeploymentResponse(status="Success", note="Deployment Successful")
    except AzureError as azure_error:
        return DeploymentResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        return DeploymentResponse(status="Fail", note=str(exception))


def get_storage_account_connection_string(account_credentials, resource_group_name, account_name):
    """Get the connection string for the storage account and file share."""
    try:
        # Create a client to the storage account.
        storage_client = StorageManagementClient(
            account_credentials["credentials"], account_credentials["subscription_id"]
        )

        # Get the storage account key.
        keys = storage_client.storage_accounts.list_keys(resource_group_name, account_name)
        print(f"Primary key for storage account: {keys.keys[0].value}")  # type: ignore

        # Create a connection string to the file share.
        conn_string = f"DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName={account_name};AccountKey={keys.keys[0].value}"  # type: ignore
        print(f"Connection string: {conn_string}")

        return DeploymentResponse(status="Success", response=conn_string, note="Deployment Successful")
    except AzureError as azure_error:
        return DeploymentResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        return DeploymentResponse(status="Fail", note=str(exception))


def get_randomized_name(prefix):
    """Get a randomized name."""
    return f"{prefix}{random.randint(1,100000):05}"


def create_storage_account(account_credentials, resource_group_name, account_name_prefix, location):
    """Create a storage account and file share."""
    try:
        # Provision the storage account, starting with a management object.
        storage_client = StorageManagementClient(
            account_credentials["credentials"], account_credentials["subscription_id"]
        )

        # Check if the account name is available. Storage account names must be unique across
        # Azure because they're used in URLs.
        number_tries = 0
        name_found = False
        account_name = get_randomized_name(account_name_prefix)
        while (name_found is False) and (number_tries < 10):
            number_tries += 1
            availability_result = storage_client.storage_accounts.check_name_availability({"name": account_name})  # type: ignore
            if availability_result.name_available:
                name_found = True
            else:
                account_name_prefix = get_randomized_name(account_name_prefix)

        if name_found is False:
            raise Exception("Unable to find an available storage account name.")

        # The name is available, so provision the account
        poller = storage_client.storage_accounts.begin_create(
            resource_group_name,
            account_name,
            {"location": location, "kind": "StorageV2", "sku": {"name": "Standard_LRS"}},  # type: ignore
        )
        # Long-running operations return a poller object; calling poller.result() waits for completion.
        account_result = poller.result()

        return DeploymentResponse(status="Success", response=account_name, note="Deployment Successful")
    except AzureError as azure_error:
        return DeploymentResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        return DeploymentResponse(status="Fail", note=str(exception))


def create_file_share(account_credentials, resource_group_name, account_name, file_share_name):
    """Create a file share in azure storage account."""
    # Provision the storage account, starting with a management object.
    try:
        storage_client = StorageManagementClient(
            account_credentials["credentials"], account_credentials["subscription_id"]
        )

        # Create a file share in the storage account.
        storage_client.file_shares.create(resource_group_name, account_name, file_share_name, {})  # type: ignore

        return DeploymentResponse(status="Success", note="Deployment Successful")
    except AzureError as azure_error:
        return DeploymentResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        return DeploymentResponse(status="Fail", note=str(exception))


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


def deploy_module(
    account_credentials, resource_group_name, module_name, virtual_machine_name, vm_size
) -> DeploymentResponse:
    """Deploy the template to a resource group."""
    try:
        print("Deploying module: ", module_name)

        # Create the resource group
        create_resource_group(account_credentials, resource_group_name, "eastus")

        template_path = os.path.join(module_name + ".json")

        with open(template_path, "r") as template_file_fd:
            template = json.load(template_file_fd)

        parameters = {
            "vmName": virtual_machine_name,
            "vmSize": vm_size,
            "vmImageResourceId": get_secret("azure_scn_image_id") + module_name,
            "adminUserName": get_secret("azure_scn_user_name"),
            "adminPassword": get_secret("azure_scn_password"),
            "subnetName": get_secret("azure_scn_subnet_name"),
            "virtualNetworkId": get_secret("azure_scn_virtual_network_id"),
        }
        deploy_status = deploy_template(account_credentials, resource_group_name, template, parameters)
        print(virtual_machine_name + " server status: ", deploy_status)

        virtual_machine_public_ip = get_ip(account_credentials, resource_group_name, virtual_machine_name + "-ip")

        return DeploymentResponse(status="Success", ip_address=virtual_machine_public_ip, note="Deployment Successful")

    except AzureError as azure_error:
        print("AzureError: ", azure_error)
        return DeploymentResponse(status="Fail", ip_address="", note=str(azure_error))
    except Exception as exception:
        print("Exception: ", exception)
        return DeploymentResponse(status="Fail", ip_address="", note=str(exception))
