import json
import os
import random
import time
import uuid

import requests
import sailazure
from azure.core.exceptions import AzureError
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.models import (DiagnosticSettingsResource, LogSettings,
                                       MetricSettings)
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountListKeysResult
from database_initialization import initialize_database
from pydantic import BaseModel, Field, StrictStr


class DeploymentResponse(BaseModel):
    """Deployment response."""

    status: StrictStr = Field(...)
    response: StrictStr = Field(default="")
    ip_address: StrictStr = Field(default="")
    note: StrictStr = Field(...)


DEV_PARAMS = {
    "azure_subscription_id": "b7a46052-b7b1-433e-9147-56efbfe28ac5",  # change this line depending on your subscription
    "vmImageResourceId": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/SAIL-PAYLOADS-ImageStorage-WUS-CVM-Rg/providers/Microsoft.Compute/galleries/sail_image_gallery/images/{0}/versions/0.0.0",
    "virtualNetworkId": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/"  # change this line depending on your subscription
    + "rg-sail-wus-dev-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-dev-01",  # change this line depending on your vnet
    "subnetName": "snet-sail-wus-dev-platformservice-01",  # change this line depending on your vnet
    "azure_scn_subnet_name": "snet-sail-wus-dev-scn-01",
    "azure_storage_resource_group": "SAIL-PAYLOADS-ImageStorage-WUS-Rg",
    "azure_storage_account_name": "sailvmimages9827",
    "azure_scn_virtual_network_id": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/rg-sail-wus-dev-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-dev-01",
}

TEST_PARAMS = {
    "azure_subscription_id": "b7a46052-b7b1-433e-9147-56efbfe28ac5",  # change this line depending on your subscription
    "vmImageResourceId": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/sail_test/providers/Microsoft.Compute/galleries/sail_image_gallery_1/images/{0}/versions/0.1.0",
    "virtualNetworkId": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/"  # change this line depending on your subscription
    + "rg-sail-wus-dev-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-dev-01",  # change this line depending on your vnet
    "subnetName": "snet-sail-wus-dev-platformservice-01",  # change this line depending on your vnet
    "azure_scn_subnet_name": "snet-sail-wus-dev-scn-01",
    "azure_storage_resource_group": "sail_test",
    "azure_storage_account_name": "sailvmimages9998",
    "azure_scn_virtual_network_id": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/rg-sail-wus-dev-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-dev-01",
}

RELEASE_CANDIDATE_PARAMS = {
    "azure_subscription_id": "40cdb551-8a8d-401f-b884-db1599022002",  # change this line depending on your subscription
    "vmImageResourceId": "/subscriptions/40cdb551-8a8d-401f-b884-db1599022002/resourceGroups/"  # change this line depending on your subscription resourcegroup where images are stored
    + "SAIL-PAYLOADS-ImageStorage-WUS-Rg/providers/Microsoft.Compute/images/",
    "virtualNetworkId": "/subscriptions/40cdb551-8a8d-401f-b884-db1599022002/resourceGroups/"  # change this line depending on your subscription
    + "rg-sail-wus-rls-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-rls-01",  # change this line depending on your vnet
    "subnetName": "snet-sail-wus-rls-platformservice-01",  # change this line depending on your vnet
    "azure_scn_subnet_name": "snet-sail-wus-rls-scn-01",
    "azure_storage_resource_group": "SAIL-PAYLOADS-ImageStorage-WUS-Rg",
    "azure_storage_account_name": "sailvmimages9828",
    "azure_scn_virtual_network_id": "/subscriptions/40cdb551-8a8d-401f-b884-db1599022002/resourceGroups/rg-sail-wus-rls-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-rls-01",
}

PRODUCTIONGA_PARAMS = {
    "azure_subscription_id": "ba383264-b9d6-4dba-b71f-58b3755382d8",  # change this line depending on your subscription
    "vmImageResourceId": "/subscriptions/ba383264-b9d6-4dba-b71f-58b3755382d8/resourceGroups/"  # change this line depending on your subscription resourcegroup where images are stored
    + "SAIL-PAYLOADS-ImageStorage-WUS-Rg/providers/Microsoft.Compute/images/",
    "virtualNetworkId": "/subscriptions/ba383264-b9d6-4dba-b71f-58b3755382d8/resourceGroups/"  # change this line depending on your subscription
    + "rg-sail-wus-prd-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-prd-01",  # change this line depending on your vnet
    "subnetName": "snet-sail-wus-prd-platformservice-01",  # change this line depending on your vnet
    "azure_scn_subnet_name": "snet-sail-wus-prd-scn-01",
    "azure_storage_resource_group": "SAIL-PAYLOADS-ImageStorage-WUS-Rg",
    "azure_storage_account_name": "sailvmimages9829",
    "azure_scn_virtual_network_id": "/subscriptions/ba383264-b9d6-4dba-b71f-58b3755382d8/resourceGroups/rg-sail-wus-prd-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-prd-01",
}

global_test_flag = True

def set_params(subscription_id, module_name, test):
    """
    Set Params based on selected subscription

    """
    parameters = {
        "vmName": module_name,
        "vmSize": "Standard_D4s_v4",
        "adminUserName": "sailuser",
        "adminPassword": "SailPassword@123",
    }

    if subscription_id == "b7a46052-b7b1-433e-9147-56efbfe28ac5":
        if test:
            parameters.update(TEST_PARAMS)
        else:
            parameters.update(DEV_PARAMS)
    elif subscription_id == "40cdb551-8a8d-401f-b884-db1599022002":
        parameters.update(RELEASE_CANDIDATE_PARAMS)
    elif subscription_id == "ba383264-b9d6-4dba-b71f-58b3755382d8":
        parameters.update(PRODUCTIONGA_PARAMS)

    return parameters


def upload_package(virtual_machine_ip, initialization_vector_file, package_file):
    headers = {"accept": "application/json"}
    files = {
        "initialization_vector": open(initialization_vector_file, "rb"),
        "bin_package": open(package_file, "rb"),
    }
    response = requests.put(
        "https://" + virtual_machine_ip + ":9090/initialization-data", headers=headers, files=files, verify=False
    )
    print("Upload package status: ", response.status_code)


def deploy_module(account_credentials, deployment_name, module_name):
    """Deploy the template to a resource group."""
    print("Deploying module: ", module_name)

    subscription_id = account_credentials["subscription_id"]

    # Each module will be deployed in a unique resource group
    resource_group_name = deployment_name + "-" + module_name

    # Create the resource group
    sailazure.create_resource_group(account_credentials, resource_group_name, "westus")

    template_path = os.path.join(os.path.dirname(__file__), "ArmTemplates", module_name + ".json")

    with open(template_path, "r") as template_file_fd:
        template = json.load(template_file_fd)

    set_parameters: dict[str, str] = set_params(subscription_id, module_name, global_test_flag)
    parameters = {
        "vmName": set_parameters["vmName"],
        "vmSize": set_parameters["vmSize"],
        "adminUserName": set_parameters["adminUserName"],
        "adminPassword": set_parameters["adminPassword"],
        "vmImageResourceId": set_parameters["vmImageResourceId"].format(module_name),
        "subnetName": set_parameters["subnetName"],
        "virtualNetworkId": set_parameters["virtualNetworkId"],
    }

    deploy_status = sailazure.deploy_template(account_credentials, resource_group_name, template, parameters)
    print(module_name + " server status: ", deploy_status)

    # virtual_machine_public_ip = sailazure.get_ip(account_credentials, resource_group_name, module_name + "-ip")
    virtual_machine_private_ip = sailazure.get_private_ip(
        account_credentials, resource_group_name, module_name + "-nic"
    )

    return virtual_machine_private_ip


def get_randomized_name(prefix: str) -> str:
    """
    Get a randomized name.

    :param prefix: The prefix for the randomized name.
    :type prefix: str
    :return: The randomized name.
    :rtype: str
    """
    return f"{prefix}{random.randint(1,100000):05}"


def deploy_key_vault(account_credentials, deployment_name, key_vault_name_prefix, storage_account_id):
    """Deploy the azure key vault"""
    # Key vault will be deployed in a unique resource group
    resource_group_name = deployment_name + "-keyvault"

    # Create a key vault name that's available because they're used in URLs.
    keyvault_client = KeyVaultManagementClient(
        credential=account_credentials["credentials"], subscription_id=account_credentials["subscription_id"]
    )

    number_tries = 0
    name_found = False
    key_vault_name = get_randomized_name(key_vault_name_prefix)
    while (name_found is False) and (number_tries < 10):
        number_tries += 1
        availability_result = keyvault_client.vaults.check_name_availability({"name": key_vault_name})  # type: ignore
        if availability_result.name_available:
            name_found = True
        else:
            key_vault_name = get_randomized_name(key_vault_name_prefix)

    if name_found is False:
        raise Exception("Unable to find an available storage account name.")

    # Create the resource group
    sailazure.create_resource_group(account_credentials, resource_group_name, "westus")

    template_path = os.path.join(os.path.dirname(__file__), "ArmTemplates", "keyvault" + ".json")

    with open(template_path, "r") as template_file_fd:
        template = json.load(template_file_fd)

    parameters = {
        "keyvault_name": key_vault_name,
        "azure_tenant_id": account_credentials["credentials"]._tenant_id,
        "azure_object_id": account_credentials["object_id"],
    }

    deploy_status = sailazure.deploy_template(account_credentials, resource_group_name, template, parameters)
    print("keyvault status: ", deploy_status)

    if deploy_status != "Succeeded":
        raise Exception("Keyvault deployment failed")

    keyvault_url = f"https://{key_vault_name}.vault.azure.net/"

    # Setup monitoring and audit logs
    key_vault_resource_id = f"/subscriptions/{account_credentials['subscription_id']}/resourceGroups/{resource_group_name}/providers/Microsoft.KeyVault/vaults/{key_vault_name}"
    monitor_client = MonitorManagementClient(
        credential=account_credentials["credentials"], subscription_id=account_credentials["subscription_id"]
    )

    diagnostic_settings_resource = DiagnosticSettingsResource(
        storage_account_id=storage_account_id,
        logs=[LogSettings(category="AuditEvent", enabled=True)],
        metrics=[MetricSettings(category="AllMetrics", enabled=True)],
    )

    monitor_client.diagnostic_settings.create_or_update(
        resource_uri=key_vault_resource_id,
        name="Key vault logs",
        parameters=diagnostic_settings_resource,
    )

    # return the url of the keyvault
    return keyvault_url


def deploy_audit_service(
    account_credentials,
    deployment_name,
    owner,
):
    """
    Deploy Audit Service
    """
    subscription_id = account_credentials["subscription_id"]

    # Get params to update json
    set_parameters = set_params(subscription_id, "auditserver", global_test_flag)
    # Deploy the frontend server
    audit_service_ip = deploy_module(account_credentials, deployment_name, "auditserver")

    # Read backend json from file and set params
    with open("auditserver.json", "r") as backend_json_fd:
        backend_json = json.load(backend_json_fd)

    backend_json["owner"] = owner

    with open("auditserver.json", "w") as outfile:
        json.dump(backend_json, outfile)

    # Sleeping for a minute
    time.sleep(60)

    upload_package(audit_service_ip, "auditserver.json", "auditserver.tar.gz")

    # Sleeping for some time
    time.sleep(90)

    return audit_service_ip


def deploy_apiservices(
    account_credentials,
    deployment_name,
    storage_account_name,
    storage_account_password,
    storage_resource_group_name,
    key_vault_url,
    owner,
    version: str,
    audit_service_ip,
):
    """
    Deploy Api Services
    """
    subscription_id = account_credentials["subscription_id"]

    # Get params to update json
    set_parameters = set_params(subscription_id, "apiservices", global_test_flag)
    # Deploy the frontend server
    apiservices_ip = deploy_module(account_credentials, deployment_name, "apiservices")

    # Read backend json from file and set params
    with open("apiservices.json", "r") as backend_json_fd:
        backend_json = json.load(backend_json_fd)
    backend_json["owner"] = owner
    backend_json["azure_subscription_id"] = subscription_id
    backend_json["azure_tenant_id"] = account_credentials["credentials"]._tenant_id
    backend_json["azure_client_id"] = account_credentials["credentials"]._client_id
    backend_json["azure_client_secret"] = account_credentials["credentials"]._client_credential
    backend_json["azure_scn_image_id"] = set_parameters["vmImageResourceId"]
    backend_json["azure_scn_subnet_name"] = set_parameters["azure_scn_subnet_name"]
    backend_json["azure_storage_resource_group"] = storage_resource_group_name
    backend_json["azure_storage_account_name"] = storage_account_name
    backend_json["azure_scn_virtual_network_id"] = set_parameters["azure_scn_virtual_network_id"]
    backend_json["azure_storage_account_password"] = storage_account_password
    backend_json["azure_keyvault_url"] = key_vault_url
    backend_json["version"] = version
    backend_json["audit_service_ip"] = audit_service_ip

    with open("apiservices.json", "w") as outfile:
        json.dump(backend_json, outfile)

    # Sleeping for a minute
    time.sleep(60)

    upload_package(apiservices_ip, "apiservices.json", "apiservices.tar.gz")

    # Sleeping for some time
    time.sleep(90)

    # Run database tools for the backend server
    initialize_database(hostname=f"https://{apiservices_ip}:8000")
    print("Api Services Database Initialization Tool run: Success")

    return apiservices_ip


def deploy_frontend(account_credentials, deployment_name, platform_services_ip):
    """Deploy the frontend server"""
    frontend_server_ip = deploy_module(account_credentials, deployment_name, "newwebfrontend")

    # Prepare the initialization vector for the frontend server
    initialization_vector = {
        "ApiServicesUrl": "https://" + platform_services_ip + ":8000",
        "VirtualMachinePublicIp": "https://" + frontend_server_ip + ":443",
    }

    with open("newwebfrontend.json", "w") as outfile:
        json.dump(initialization_vector, outfile)

    # Sleeping for two minutes
    time.sleep(90)

    upload_package(frontend_server_ip, "newwebfrontend.json", "newwebfrontend.tar.gz")

    return frontend_server_ip


def create_storage_account(account_credentials: dict, deployment_name: str, account_name_prefix: str, location: str):
    """
    Create a storage account and file share.

    :param account_credentials: The account credentials.
    :type account_credentials: dict
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
        storage_client = StorageManagementClient(
            account_credentials["credentials"], account_credentials["subscription_id"]
        )

        # Each module will be deployed in a unique resource group
        resource_group_name = deployment_name + "-storage"

        # Create the resource group
        sailazure.create_resource_group(account_credentials, resource_group_name, location)

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

        # Get the storage account key
        keys: StorageAccountListKeysResult = storage_client.storage_accounts.list_keys(resource_group_name, account_name)  # type: ignore
        storage_account_key: str = keys.keys[0].value  # type: ignore

        return (
            DeploymentResponse(status="Success", response=account_name, note="Deployment Successful"),
            account_name,
            storage_account_key,
            resource_group_name,
        )
    except AzureError as azure_error:
        return DeploymentResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        return DeploymentResponse(status="Fail", note=str(exception))


def update_firewall(deployment_name, module_name, private_ip_address):
    """
    Update Firewall with a new public ipfor new deployment and ammend dnat rules to allow access
    """
    module_fw_info = {}
    # Authenticate the azure credentials for SAIL GLOBAL HUB
    account_credentials = sailazure.authenticate(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID, "6e7f356c-6059-4799-b83a-c4744e4a7c2e"
    )
    print("\n\n===============================================================")
    print("UPDATING FIREWALL")
    print("===============================================================")
    print("\n\n===============================================================")
    print(f"Creating new Firewall Public IP Address for {module_name} public endpoint")
    print("===============================================================")
    # Create the firewall public ips for platform
    pip_name = "PIP" + "-" + deployment_name + "-" + module_name
    firewall_ip_name, firewall_ip, firewall_ip_id = sailazure.create_public_ip(
        account_credentials, "rg-sail-wus-hubpipdev-001", "westus", pip_name
    )
    module_fw_info[module_name + "-firewall_ip_name"] = firewall_ip_name
    module_fw_info[module_name + "-firewall_ip"] = firewall_ip
    module_fw_info[module_name + "-firewall_ip_id"] = firewall_ip_id
    print(f"{module_name}'s firewall public ip name : {firewall_ip_name}")
    print(f"{module_name}'s firewall public ip : {firewall_ip}")
    print(f"{module_name}'s firewall public ip id : {firewall_ip_id}")

    async_updated_fw_pip_result, firewall_ip_id, firewall_ip_name, = sailazure.update_fw_pip(
        account_credentials,
        firewall_ip_id,
        firewall_ip_name,
    )
    print("\n===============================================================\n")
    print(
        f"Updated azure firewall Information:\n{async_updated_fw_pip_result}\nfirewall_ip_id:\n{firewall_ip_id}firewall_ip_name:\n{firewall_ip_name}firewall_ip:\n{firewall_ip}"
    )
    print("\n\n===============================================================")
    print(f"Updating new Firewall DNAT RULES for {module_name}")
    print("===============================================================")
    # Update DNAT Rules per module
    async_updated_fw_pol_result = sailazure.update_fw_dnat_rules(
        account_credentials,
        firewall_ip_name,
        firewall_ip,
        private_ip_address,
        module_name,
    )
    print("\n===============================================================\n")
    print(f"{module_name}'s Azure Firewall DNAT RULES result:\n{async_updated_fw_pol_result}")

    print("\n\n===============================================================")
    print("ENDING FUNCTION UPDATE_FIREWALL")
    print("===============================================================")
    return module_fw_info, async_updated_fw_pip_result


if __name__ == "__main__":
    AZURE_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")
    AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID")
    AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
    AZURE_OBJECT_ID = os.environ.get("AZURE_OBJECT_ID")
    AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
    OWNER = os.environ.get("OWNER")
    PURPOSE = os.environ.get("PURPOSE")
    VERSION = os.environ.get("VERSION")

    # Check if public ip is required
    public_ip = False
    if "PUBLIC_IP" in os.environ:
        public_ip = os.getenv("PUBLIC_IP", "False") == "True"

    if not OWNER or not PURPOSE:
        print("Please set the OWNER and PURPOSE environment variables")
        exit(1)
    deployment_id = OWNER + "-" + str(uuid.uuid1()) + "-" + PURPOSE

    # Authenticate the azure credentials
    account_credentials = sailazure.authenticate(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID
    )
    account_credentials["object_id"] = AZURE_OBJECT_ID

    # Deploy Storage Account
    (
        storage_account,
        storage_account_name,
        storage_accout_password,
        storage_resource_group_name,
    ) = create_storage_account(account_credentials, deployment_id, "saildatastorage", "westus")

    # Create storage account id
    storage_account_id = (
        "/subscriptions/"
        + account_credentials["subscription_id"]
        + "/resourceGroups/"
        + storage_resource_group_name
        + "/providers/Microsoft.Storage/storageAccounts/"
        + storage_account_name
    )

    # Provision a key vault
    key_vault_url = deploy_key_vault(
        account_credentials=account_credentials,
        deployment_name=deployment_id,
        key_vault_name_prefix="sailkeyvault",
        storage_account_id=storage_account_id,
    )

    # Deploy the audit services
    audit_service_ip = deploy_audit_service(
        account_credentials,
        deployment_id,
        OWNER,
    )
    print("Audit Service server: ", audit_service_ip)

    # Deploy the API services
    platform_services_ip = deploy_apiservices(
        account_credentials,
        deployment_id,
        storage_account_name,
        storage_accout_password,
        storage_resource_group_name,
        key_vault_url,
        OWNER,
        VERSION,
        audit_service_ip,
    )
    print("API Services server: ", platform_services_ip)

    # Commented out deployment of webfrontend as not used atm BOARD-2148
    # # Deploy the frontend server
    # frontend_ip = deploy_frontend(
    #     account_credentials,
    #     deployment_id,
    #     platform_services_ip,
    # )
    # print("Frontend server: ", frontend_ip)

    # Deploy Firewall IPv4Address and update DNAT Rules
    if public_ip:
        api_fw_info, async_updated_fw_pip_result = update_firewall(deployment_id, "apiservices", platform_services_ip)
        # web_fw_info, async_updated_fw_pip_result = update_firewall(deployment_id, "newwebfrontend", frontend_ip)

        # Summary
        print("\n\n===============================================================")
        print("================= SUMMARY: Deploy Firewall =====================")
        print(f"apiservices-firewall_ip_name: {api_fw_info['apiservices-firewall_ip_name']}")
        print(f"apiservices-firewall_ip: {api_fw_info['apiservices-firewall_ip']}")
        print(f"apiservices-firewall_ip_id: {api_fw_info['apiservices-firewall_ip_id']}")
        # print(f"newwebfrontend-firewall_ip_name: {web_fw_info['newwebfrontend-firewall_ip_name']}")
        # print(f"newwebfrontend-firewall_ip: {web_fw_info['newwebfrontend-firewall_ip']}")
        # print(f"newwebfrontend-firewall_ip_id: {web_fw_info['newwebfrontend-firewall_ip_id']}")
        print(
            f"Current Azure Firewall Information:\n {json.dumps(async_updated_fw_pip_result.as_dict(), indent=4, sort_keys=True)}"
        )
    print("\n\n===============================================================")
    print("================= SUMMARY: Deploy Platform =====================")
    # print(f"Deployment complete. Please visit the link to access the internal demo: https://{frontend_ip}")
    # print(
    #     f"Deployment complete. Please visit the link to access the public demo: https://{web_fw_info['newwebfrontend-firewall_ip']}"
    # )
    print(f"SAIL API Services is hosted internally on: https://{platform_services_ip}:8000")
    if public_ip:
        print(f"SAIL API Services is hosted externally on: https://{api_fw_info['apiservices-firewall_ip']}:8000")
    print(f"Deployment ID: {deployment_id}")
    print("Kindly delete all the resource group created on azure with the deployment ID.")
    print("===============================================================\n\n")

    # Delete the resource group for the backend server
    # sailazure.delete_resouce_group(account_credentials, deployment_id + "backend")
