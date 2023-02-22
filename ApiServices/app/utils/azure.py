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
from base64 import b64decode, b64encode
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from azure.core.exceptions import AzureError
from azure.core.polling import AsyncLROPoller
from azure.identity.aio import ClientSecretCredential
from azure.keyvault.keys.aio import KeyClient
from azure.keyvault.keys.crypto.aio import KeyWrapAlgorithm
from azure.keyvault.secrets.aio import SecretClient
from azure.mgmt.network.aio import NetworkManagementClient
from azure.mgmt.resource.resources.aio import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode, ResourceGroup
from azure.mgmt.storage.aio import StorageManagementClient
from azure.storage.fileshare import FileSasPermissions, generate_file_sas
from azure.storage.fileshare.aio import ShareDirectoryClient
from pydantic import BaseModel, Field, StrictStr

from app.utils.secrets import get_secret
from models.common import KeyVaultObject


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


@dataclass
class AzureCredentials:
    """Azure credentials."""

    credentials: ClientSecretCredential
    subscription_id: str
    location: str


async def authentication_shared_access_signature(
    account_credentials: AzureCredentials,
    account_name: str,
    resource_group_name: str,
    file_path: str,
    share_name: str,
    permission: str,
    expiry: datetime,
):
    """
    Get the connection string for the storage account and file share.

    :param account_credentials: The account credentials.
    :type account_credentials: AzureCredentials
    :param account_name: The account name.
    :type account_name: str
    :param resource_group_name: The resource group name.
    :type resource_group_name: str
    :param file_path: The file path.
    :type file_path: str
    :param share_name: The share name.
    :type share_name: str
    :param permission: The permission for the resource.
    :type permission: str
    :param expiry: The expiry.
    :type expiry: datetime
    :return: The response with status and sas_token.
    :rtype: DeploymentResponse
    """
    try:
        # Create a client to the storage account.
        storage_client = StorageManagementClient(
            credential=account_credentials.credentials, subscription_id=account_credentials.subscription_id  # type: ignore
        )

        # Get the storage account key.
        keys = await storage_client.storage_accounts.list_keys(resource_group_name, account_name)

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


async def file_share_create_directory(
    connection_string: str, file_share_name: str, directory_name: str
) -> DeploymentResponse:
    """
    Create a directory in the file share.

    :param connection_string: Connection String to authenticate access
    :type connection_string: str
    :param file_share_name: the name of the fileshare to put the file into
    :type file_share_name: str
    :param directory_name: the directory name in the file share to be created
    :type directory_name: str
    :return: status of file creation
    :rtype: DeploymentResponse
    """

    try:
        directory_client = ShareDirectoryClient.from_connection_string(
            conn_str=connection_string, share_name=file_share_name, directory_path=directory_name
        )
        create_response = await directory_client.create_directory()  # type: ignore

        return DeploymentResponse(status="Success", note="Deployment Successful")
    except AzureError as azure_error:
        return DeploymentResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        return DeploymentResponse(status="Fail", note=str(exception))


async def get_storage_account_connection_string(
    account_credentials: AzureCredentials, resource_group_name: str, account_name: str
) -> DeploymentResponse:
    """
    Get the connection string for the storage account and file share.

    :param account_credentials: user account credentials
    :type account_credentials: AzureCredentials
    :param resource_group_name: The resource group name.
    :type resource_group_name: str
    :param account_name: The account name.
    :type account_name: str
    :return: The response with status and connection string.
    :rtype: DeploymentResponse
    """
    try:
        # Create a client to the storage account.
        storage_client = StorageManagementClient(account_credentials.credentials, account_credentials.subscription_id)  # type: ignore

        # Get the storage account key.
        keys = await storage_client.storage_accounts.list_keys(resource_group_name, account_name)

        # Create a connection string to the file share.
        conn_string = f"DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName={account_name};AccountKey={keys.keys[0].value}"  # type: ignore

        return DeploymentResponse(status="Success", response=conn_string, note="Deployment Successful")
    except AzureError as azure_error:
        return DeploymentResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        return DeploymentResponse(status="Fail", note=str(exception))


async def get_randomized_name(prefix: str) -> str:
    """
    Get a randomized name.

    :param prefix: The prefix for the randomized name.
    :type prefix: str
    :return: The randomized name.
    :rtype: str
    """
    return f"{prefix}{random.randint(1,100000):05}"


async def create_storage_account(
    account_credentials: AzureCredentials, resource_group_name: str, account_name_prefix: str, location: str
) -> DeploymentResponse:
    """
    Create a storage account and file share.

    :param account_credentials: The account credentials.
    :type account_credentials: AzureCredentials
    :param resource_group_name: The resource group name.
    :type resource_group_name: str
    :param account_name_prefix: The account name prefix.
    :type account_name_prefix: str
    :param location: The location.
    :type location: str
    :raises Exception: If the storage account creation fails.
    :return: The response with status and account name.
    :rtype: DeploymentResponse
    """
    try:
        # Provision the storage account, starting with a management object.
        storage_client = StorageManagementClient(account_credentials.credentials, account_credentials.subscription_id)  # type: ignore

        # Check if the account name is available. Storage account names must be unique across
        # Azure because they're used in URLs.
        number_tries = 0
        name_found = False
        account_name = await get_randomized_name(account_name_prefix)
        while (name_found is False) and (number_tries < 10):
            number_tries += 1
            availability_result = await storage_client.storage_accounts.check_name_availability({"name": account_name})  # type: ignore
            if availability_result.name_available:
                name_found = True
            else:
                account_name_prefix = await get_randomized_name(account_name_prefix)

        if name_found is False:
            raise Exception("Unable to find an available storage account name.")

        # The name is available, so provision the account
        await storage_client.storage_accounts.begin_create(
            resource_group_name,
            account_name,
            {"location": location, "kind": "StorageV2", "sku": {"name": "Standard_LRS"}},  # type: ignore
        )

        return DeploymentResponse(status="Success", response=account_name, note="Deployment Successful")
    except AzureError as azure_error:
        return DeploymentResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        return DeploymentResponse(status="Fail", note=str(exception))


async def create_file_share(
    account_credentials: AzureCredentials, resource_group_name: str, account_name: str, file_share_name: str
) -> DeploymentResponse:
    """
    Create a file share in azure storage account.

    :param account_credentials: The account credentials.
    :type account_credentials: AzureCredentials
    :param resource_group_name: The resource group name.
    :type resource_group_name: str
    :param account_name: The account name.
    :type account_name: str
    :param file_share_name: The file share name.
    :type file_share_name: str
    :return: The response with status and file share name.
    :rtype: DeploymentResponse
    """
    try:
        storage_client = StorageManagementClient(account_credentials.credentials, account_credentials.subscription_id)  # type: ignore

        # Create a file share in the storage account.
        await storage_client.file_shares.create(resource_group_name, account_name, file_share_name, {})  # type: ignore

        return DeploymentResponse(status="Success", note="Deployment Successful")
    except AzureError as azure_error:
        return DeploymentResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        return DeploymentResponse(status="Fail", note=str(exception))


async def create_resource_group(account_credentials: AzureCredentials, resource_group_name: str):
    """
    Deploy the template to a resource group.

    :param account_credentials: The account credentials.
    :type account_credentials: AzureCredentials
    :param resource_group_name: The resource group name.
    :type resource_group_name: str
    :param location: The location.
    :type location: str
    :return: provisioning state of the resource group.
    :rtype: str
    """
    module_name = resource_group_name.split("-")[-1]
    client = ResourceManagementClient(account_credentials.credentials, account_credentials.subscription_id)  # type: ignore
    response: ResourceGroup = await client.resource_groups.create_or_update(
        resource_group_name,
        {
            "location": account_credentials.location,
            "tags": {
                "module": module_name,
            },
        },
    )  # type: ignore
    return response.properties.provisioning_state  # type: ignore


async def authenticate() -> AzureCredentials:
    """
    Authenticate using client_id and client_secret.

    :return: The credentials and subscription id.
    :rtype: dict
    """

    credentials = ClientSecretCredential(
        client_id=get_secret("azure_client_id"),
        client_secret=get_secret("azure_client_secret"),
        tenant_id=get_secret("azure_tenant_id"),
    )
    return AzureCredentials(
        credentials=credentials, subscription_id=get_secret("azure_subscription_id"), location="westus"
    )


async def deploy_template(
    account_credentials: AzureCredentials, resource_group_name: str, template: str, parameters: dict
):
    """
    Deploy the template to a resource group.

    :param account_credentials: The account credentials.
    :type account_credentials: str
    :param resource_group_name: The resource group name.
    :type resource_group_name: str
    :param template: The azure arm template.
    :type template: str
    :param parameters: The parameters for the template.
    :type parameters: dict
    :return: The deployment response.
    """
    client = ResourceManagementClient(account_credentials.credentials, account_credentials.subscription_id)  # type: ignore

    parameters = {k: {"value": v} for k, v in parameters.items()}
    deployment_properties = {
        "mode": DeploymentMode.incremental,
        "template": template,
        "parameters": parameters,
    }

    # Get a unique deployment name
    deployment_name = await get_randomized_name("deployment")

    # Deploy the template
    deployment_state: AsyncLROPoller = await client.deployments.begin_create_or_update(
        resource_group_name, deployment_name, {"properties": deployment_properties}  # type: ignore
    )

    # Wait for the deployment to complete
    await deployment_state.wait()


async def delete_resouce_group(account_credentials: AzureCredentials, resource_group_name: str) -> DeleteResponse:
    """
    Delete the resource group.

    :param account_credentials: The account credentials.
    :type account_credentials: str
    :param resource_group_name: The resource group name.
    :type resource_group_name: str
    :return: The delete response.
    :rtype: DeleteResponse
    """
    try:
        client = ResourceManagementClient(account_credentials.credentials, account_credentials.subscription_id)  # type: ignore
        delete_async_operation = await client.resource_groups.begin_delete(resource_group_name)

        return DeleteResponse(status="Success", note="")
    except AzureError as azure_error:
        return DeleteResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        return DeleteResponse(status="Fail", note=str(exception))


async def get_ip(account_credentials: AzureCredentials, resource_group_name: str, ip_resource_name: str) -> str:
    """
    Get the IP address of the resource.

    :param account_credentials: The account credentials.
    :type account_credentials: AzureCredentials
    :param resource_group_name: The resource group name.
    :type resource_group_name: str
    :param ip_resource_name: The ip resource name.
    :type ip_resource_name: str
    :return: The ip address.
    :rtype: str
    """
    client = NetworkManagementClient(account_credentials.credentials, account_credentials.subscription_id)  # type: ignore
    foo = await client.public_ip_addresses.get(resource_group_name, ip_resource_name)
    return foo.ip_address


async def get_private_ip(
    account_credentials: AzureCredentials, resource_group_name: str, network_interface_name: str
) -> str:
    """
    Get the private IP address of the resource.

    :param account_credentials: The account credentials.
    :type account_credentials: AzureCredentials
    :param resource_group_name: The resource group name.
    :type resource_group_name: str
    :param network_interface_name: The network interface name.
    :type network_interface_name: str
    :return: The private ip address.
    :rtype: str
    """
    client = NetworkManagementClient(account_credentials.credentials, account_credentials.subscription_id)  # type: ignore
    network_interfaces = await client.network_interfaces.get(resource_group_name, network_interface_name)
    return network_interfaces.ip_configurations[0].private_ip_address


async def deploy_module(
    account_credentials: AzureCredentials,
    resource_group_name: str,
    virtual_machine_name: str,
    vm_size: str,
    custom_data: str,
) -> DeploymentResponse:
    """
    Deploy the template to a resource group.

    :param account_credentials: The account credentials.
    :type account_credentials: AzureCredentials
    :param resource_group_name: The resource group name.
    :type resource_group_name: str
    :param virtual_machine_name: The name of the virtual machine.
    :type virtual_machine_name: str
    :param vm_size: The azure specific vm size.
    :type vm_size: str
    :param custom_data: The custom data to pass to the vm.
    :type custom_data: str
    :return: The deployment response.
    :rtype: DeploymentResponse
    """
    try:
        # Create the resource group
        await create_resource_group(account_credentials, resource_group_name)

        # Provision the secure computation node
        if vm_size == "Standard_DC4ads_v5":
            template_path = "sailvm-cvm.json"
        else:
            template_path = "sailvm.json"

        with open(template_path, "r") as template_file_fd:
            template = json.load(template_file_fd)

        parameters = {
            "vmName": virtual_machine_name,
            "vmSize": vm_size,
            "vmImageResourceId": get_secret("azure_scn_image_id"),
            "adminUserName": get_secret("azure_scn_user_name"),
            "adminPassword": get_secret("azure_scn_password"),
            "subnetName": get_secret("azure_scn_subnet_name"),
            "virtualNetworkId": get_secret("azure_scn_virtual_network_id"),
            "customData": custom_data,
        }
        await deploy_template(account_credentials, resource_group_name, template, parameters)

        virtual_machine_public_ip = await get_private_ip(
            account_credentials, resource_group_name, virtual_machine_name + "-nic"
        )

        return DeploymentResponse(status="Success", ip_address=virtual_machine_public_ip, note="Deployment Successful")

    except AzureError as azure_error:
        return DeploymentResponse(status="Fail", ip_address="", note=str(azure_error))
    except Exception as exception:
        return DeploymentResponse(status="Fail", ip_address="", note=str(exception))


async def create_rsa_key(
    account_credentials: AzureCredentials, key_name: str, key_size: int
) -> Optional[KeyVaultObject]:
    """
    Create an RSA key of given size(minimum 3072).

    :param account_credentials: The account credentials.
    :type account_credentials: AzureCredentials
    """
    key_client = KeyClient(vault_url=get_secret("azure_keyvault_url"), credential=account_credentials.credentials)  # type: ignore

    if key_size < 3072:
        raise ValueError("Key size must be at least 3072 bits.")

    # Create an RSA key
    rsa_key = await key_client.create_rsa_key(key_name, size=key_size)

    if not rsa_key.properties.version:
        raise ValueError("Key version is not set.")

    return KeyVaultObject(name=key_name, version=rsa_key.properties.version)


async def wrap_aes_key(aes_key: bytes, wrapping_key: KeyVaultObject) -> Optional[KeyVaultObject]:
    """
    Wrap the AES key with the RSA key and then store it in the keyvault.

    :param account_credentials: The account credentials.
    :type account_credentials: AzureCredentials
    :param aes_key: The AES key.
    :type aes_key: bytes
    :param rsa_key_id: The RSA key id.
    :type rsa_key_id: str
    """
    # Authenticate to Azure
    account_credentials = await authenticate()

    # Wrap the AES key with the RSA key
    key_client = KeyClient(vault_url=get_secret("azure_keyvault_url"), credential=account_credentials.credentials)  # type: ignore

    # There is an option to add the key version to the key name, but it is not required.
    crypto_client = key_client.get_cryptography_client(key_name=wrapping_key.name, key_version=wrapping_key.version)

    # Wrap the AES key with the RSA key
    wrapped_aes_key = await crypto_client.wrap_key(KeyWrapAlgorithm.rsa_oaep_256, aes_key)

    # Store the wrapped AES key in the keyvault as a secret
    secret_client = SecretClient(vault_url=get_secret("azure_keyvault_url"), credential=account_credentials.credentials)  # type: ignore
    encoded_key = b64encode(wrapped_aes_key.encrypted_key).decode("ascii")

    # The secret is created with the same name as the wrapping key
    secret_set_response = await secret_client.set_secret(wrapping_key.name, encoded_key)

    if not secret_set_response.name or not secret_set_response.properties.version:
        raise ValueError("Secret name or version is not set.")

    return KeyVaultObject(name=secret_set_response.name, version=secret_set_response.properties.version)


async def unwrap_aes_with_rsa_key(wrapped_aes_key: KeyVaultObject, wrapping_key: KeyVaultObject) -> bytes:
    """
    Unwrap the AES key with the RSA key.

    :param account_credentials: The account credentials.
    :type account_credentials: AzureCredentials
    :param wrapped_aes_key: The wrapped AES key.
    :type wrapped_aes_key: bytes
    :param rsa_key_id: The RSA key id.
    :type rsa_key_id: str
    :return: The unwrapped AES key.
    :rtype: bytes
    """
    # Authenticate to Azure
    account_credentials = await authenticate()

    # Get the secret from the keyvault
    secret_client = SecretClient(vault_url=get_secret("azure_keyvault_url"), credential=account_credentials.credentials)  # type: ignore
    secret_get_response = await secret_client.get_secret(name=wrapped_aes_key.name, version=wrapped_aes_key.version)

    # UnWrap the secret with the RSA key
    key_client = KeyClient(vault_url=get_secret("azure_keyvault_url"), credential=account_credentials.credentials)  # type: ignore
    crypto_client = key_client.get_cryptography_client(key_name=wrapping_key.name, key_version=wrapping_key.version)

    if not secret_get_response.value:
        raise ValueError("Secret value is not set.")

    unwrapped_aes_key = await crypto_client.unwrap_key(
        KeyWrapAlgorithm.rsa_oaep_256, b64decode(secret_get_response.value.encode("ascii"))
    )

    return unwrapped_aes_key.key
