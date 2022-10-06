import json
import os
import random
import subprocess
import time
import uuid
from re import sub

import requests
from azure.core.exceptions import AzureError
from azure.mgmt.storage import StorageManagementClient
from pydantic import BaseModel, Field, StrictStr

import sailazure

FINAL_DEV_PARAMS = {
    "azure_subscription_id": "b7a46052-b7b1-433e-9147-56efbfe28ac5",  # change this line depending on your subscription
    "vmImageResourceId": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/"  # change this line depending on your subscription resourcegroup where images are stored
    + "SAIL-PAYLOADS-3183eaf-ImageStorage-WUS-Rg/providers/Microsoft.Compute/images/",
    "virtualNetworkId": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/"  # change this line depending on your subscription
    + "rg-sail-wus-dev-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-dev-01",  # change this line depending on your vnet
    "subnetName": "snet-sail-wus-dev-platformservice-01",  # change this line depending on your vnet
    "azure_scn_image_id": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/SAIL-PAYLOADS-ImageStorage-WUS-Rg/providers/Microsoft.Compute/images/",
    "azure_scn_subnet_name": "snet-sail-wus-dev-scn-01",
    "azure_storage_resource_group": "SAIL-PAYLOADS-ImageStorage-WUS-Rg",
    "azure_storage_account_name": "sailvmimages9827",
    "azure_scn_virtual_network_id": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/rg-sail-wus-dev-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-dev-01",
}

FINAL_RELEASE_CANDIDATE_PARAMS = {
    "azure_subscription_id": "40cdb551-8a8d-401f-b884-db1599022002",  # change this line depending on your subscription
    "vmImageResourceId": "/subscriptions/40cdb551-8a8d-401f-b884-db1599022002/resourceGroups/"  # change this line depending on your subscription resourcegroup where images are stored
    + "InitializerImageStorage-WUS-Rg/providers/Microsoft.Compute/images/",
    "virtualNetworkId": "/subscriptions/40cdb551-8a8d-401f-b884-db1599022002/resourceGroups/"  # change this line depending on your subscription
    + "rg-sail-wus-rls-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-rls-01",  # change this line depending on your vnet
    "subnetName": "snet-sail-wus-rls-platformservice-01",  # change this line depending on your vnet
    "azure_scn_image_id": "/subscriptions/40cdb551-8a8d-401f-b884-db1599022002/resourceGroups/SAIL-PAYLOADS-ImageStorage-WUS-Rg/providers/Microsoft.Compute/images/",
    "azure_scn_subnet_name": "snet-sail-wus-rls-scn-01",
    "azure_storage_resource_group": "SAIL-PAYLOADS-ImageStorage-WUS-Rg",
    "azure_storage_account_name": "sailvmimages9828",
    "azure_scn_virtual_network_id": "/subscriptions/40cdb551-8a8d-401f-b884-db1599022002/resourceGroups/rg-sail-wus-rls-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-rls-01",
}

FINAL_PRODUCTIONGA_PARAMS = {
    "azure_subscription_id": "ba383264-b9d6-4dba-b71f-58b3755382d8",  # change this line depending on your subscription
    "vmImageResourceId": "/subscriptions/ba383264-b9d6-4dba-b71f-58b3755382d8/resourceGroups/"  # change this line depending on your subscription resourcegroup where images are stored
    + "InitializerImageStorage-WUS-Rg/providers/Microsoft.Compute/images/",
    "virtualNetworkId": "/subscriptions/ba383264-b9d6-4dba-b71f-58b3755382d8/resourceGroups/"  # change this line depending on your subscription
    + "rg-sail-wus-prd-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-prd-01",  # change this line depending on your vnet
    "subnetName": "snet-sail-wus-prd-platformservice-01",  # change this line depending on your vnet
    "azure_scn_image_id": "/subscriptions/ba383264-b9d6-4dba-b71f-58b3755382d8/resourceGroups/SAIL-PAYLOADS-ImageStorage-WUS-Rg/providers/Microsoft.Compute/images/",
    "azure_scn_subnet_name": "snet-sail-wus-prd-scn-01",
    "azure_storage_resource_group": "SAIL-PAYLOADS-ImageStorage-WUS-Rg",
    "azure_storage_account_name": "sailvmimages9829",
    "azure_scn_virtual_network_id": "/subscriptions/ba383264-b9d6-4dba-b71f-58b3755382d8/resourceGroups/rg-sail-wus-prd-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-prd-01",
}


def set_params(subscription_id, module_name):
    """
    Set Params based on selected subscription

    """
    development_parameters = {
        "azure_subscription_id": FINAL_DEV_PARAMS["azure_subscription_id"],
        "vmImageResourceId": FINAL_DEV_PARAMS["vmImageResourceId"] + module_name,
        "virtualNetworkId": FINAL_DEV_PARAMS["virtualNetworkId"],  # change this line depending on your subscription
        "subnetName": FINAL_DEV_PARAMS["subnetName"],  # change this line depending on your vnet
        "azure_scn_image_id": FINAL_DEV_PARAMS["azure_scn_image_id"],
        "azure_scn_subnet_name": FINAL_DEV_PARAMS["azure_scn_subnet_name"],
        "azure_storage_resource_group": FINAL_DEV_PARAMS["azure_storage_resource_group"],
        "azure_storage_account_name": FINAL_DEV_PARAMS["azure_storage_account_name"],
        "azure_scn_virtual_network_id": FINAL_DEV_PARAMS["azure_scn_virtual_network_id"],
    }

    release_candidate_parameters = {
        "azure_subscription_id": FINAL_RELEASE_CANDIDATE_PARAMS["azure_subscription_id"],
        "vmImageResourceId": FINAL_RELEASE_CANDIDATE_PARAMS["vmImageResourceId"] + module_name,
        "virtualNetworkId": FINAL_RELEASE_CANDIDATE_PARAMS["virtualNetworkId"],
        "subnetName": FINAL_RELEASE_CANDIDATE_PARAMS["subnetName"],  # change this line depending on your vnet
        "azure_scn_image_id": FINAL_RELEASE_CANDIDATE_PARAMS["azure_scn_image_id"],
        "azure_scn_subnet_name": FINAL_RELEASE_CANDIDATE_PARAMS["azure_scn_subnet_name"],
        "azure_storage_resource_group": FINAL_RELEASE_CANDIDATE_PARAMS["azure_storage_resource_group"],
        "azure_storage_account_name": FINAL_RELEASE_CANDIDATE_PARAMS["azure_storage_account_name"],
        "azure_scn_virtual_network_id": FINAL_RELEASE_CANDIDATE_PARAMS["azure_scn_virtual_network_id"],
    }

    productionGA_parameters = {
        "azure_subscription_id": FINAL_PRODUCTIONGA_PARAMS["azure_subscription_id"],
        "vmImageResourceId": FINAL_PRODUCTIONGA_PARAMS["vmImageResourceId"] + module_name,
        "virtualNetworkId": FINAL_PRODUCTIONGA_PARAMS["virtualNetworkId"],
        "subnetName": FINAL_PRODUCTIONGA_PARAMS["subnetName"],
        "azure_scn_image_id": FINAL_PRODUCTIONGA_PARAMS["azure_scn_image_id"],
        "azure_scn_subnet_name": FINAL_PRODUCTIONGA_PARAMS["azure_scn_subnet_name"],
        "azure_storage_resource_group": FINAL_PRODUCTIONGA_PARAMS["azure_storage_resource_group"],
        "azure_storage_account_name": FINAL_PRODUCTIONGA_PARAMS["azure_storage_account_name"],
        "azure_scn_virtual_network_id": FINAL_PRODUCTIONGA_PARAMS["azure_scn_virtual_network_id"],
    }

    parameters = {
        "vmName": module_name,
        "vmSize": "Standard_D4s_v4",
        "adminUserName": "sailuser",
        "adminPassword": "SailPassword@123",
    }

    if subscription_id == "b7a46052-b7b1-433e-9147-56efbfe28ac5":
        parameters.update(development_parameters)
    elif subscription_id == "40cdb551-8a8d-401f-b884-db1599022002":
        parameters.update(release_candidate_parameters)
    elif subscription_id == "ba383264-b9d6-4dba-b71f-58b3755382d8":
        parameters.update(productionGA_parameters)

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


def deploy_module(account_credentials, deployment_name, module_name, subscription_id):
    """Deploy the template to a resource group."""
    print("Deploying module: ", module_name)

    # Each module will be deployed in a unique resource group
    resource_group_name = deployment_name + "-" + module_name

    # Create the resource group
    sailazure.create_resource_group(account_credentials, resource_group_name, "westus")

    template_path = os.path.join(os.path.dirname(__file__), "ArmTemplates", module_name + ".json")

    with open(template_path, "r") as template_file_fd:
        template = json.load(template_file_fd)

    set_parameters = set_params(subscription_id, module_name)
    parameters = {
        "vmName": module_name,
        "vmSize": "Standard_D4s_v4",
        "adminUserName": "sailuser",
        "adminPassword": "SailPassword@123",
        "vmImageResourceId": set_parameters["vmImageResourceId"] + module_name,
        "subnetName": set_parameters["subnetName"],
        "virtualNetworkId": set_parameters["virtualNetworkId"],
    }

    deploy_status = sailazure.deploy_template(account_credentials, resource_group_name, template, parameters)
    print(module_name + " server status: ", deploy_status)

    virtual_machine_public_ip = sailazure.get_ip(account_credentials, resource_group_name, module_name + "-ip")

    return virtual_machine_public_ip


def deploy_apiservices(account_credentials, deployment_name, owner, subscription_id):
    """
    Deploy Api Services

    """
    # Get params to update json
    set_parameters = set_params(subscription_id, "apiservices")
    # Deploy the frontend server
    apiservices_ip = deploy_module(account_credentials, deployment_name, "apiservices", subscription_id)

    # Read backend json from file and set params
    with open("apiservices.json", "r") as backend_json_fd:
        backend_json = json.load(backend_json_fd)
    backend_json["owner"] = owner
    backend_json["azure_subscription_id"] = set_parameters["azure_subscription_id"]
    backend_json["azure_scn_image_id"] = set_parameters["azure_scn_image_id"]
    backend_json["azure_scn_subnet_name"] = set_parameters["azure_scn_subnet_name"]
    backend_json["azure_storage_resource_group"] = set_parameters["azure_storage_resource_group"]
    backend_json["azure_storage_account_name"] = set_parameters["azure_storage_account_name"]
    backend_json["azure_scn_virtual_network_id"] = set_parameters["azure_scn_virtual_network_id"]

    with open("apiservices.json", "w") as outfile:
        json.dump(backend_json, outfile)

    # Sleeping for a minute
    time.sleep(60)

    upload_package(apiservices_ip, "apiservices.json", "apiservices.tar.gz")

    # Sleeping for some time
    time.sleep(90)

    # Run database tools for the backend server
    database_tools_run = subprocess.run(
        [
            "./DatabaseInitializationTool",
            "--ip=" + apiservices_ip,
            "--settings=./DatabaseInitializationSettings.json",
            "--allsteps",
        ],
        stdout=subprocess.PIPE,
    )
    print("Api Services Database Initialization Tool run: ", database_tools_run)

    return apiservices_ip


def deploy_frontend(account_credentials, deployment_name, platform_services_ip, subscription_id):
    # Deploy the frontend server
    frontend_server_ip = deploy_module(account_credentials, deployment_name, "newwebfrontend", subscription_id)

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


def deploy_orchestrator(account_credentials, deployment_name):
    # Deploy the orchestrator server
    orchestrator_server_ip = deploy_module(account_credentials, deployment_name, "orchestrator")

    # There is no initialization vector for the orchestrator
    initialization_vector = {"apiservicesUrl": "https://" + platform_services_ip + ":8000"}

    with open("orchestrator.json", "w") as outfile:
        json.dump(initialization_vector, outfile)

    upload_package(orchestrator_server_ip, "orchestrator.json", "orchestrator.tar.gz")

    return orchestrator_server_ip


class DeploymentResponse(BaseModel):
    """Deployment response."""

    status: StrictStr = Field(...)
    response: StrictStr = Field(default="")
    ip_address: StrictStr = Field(default="")
    note: StrictStr = Field(...)


def get_randomized_name(prefix: str) -> str:
    """
    Get a randomized name.

    :param prefix: The prefix for the randomized name.
    :type prefix: str
    :return: The randomized name.
    :rtype: str
    """
    return f"{prefix}{random.randint(1,100000):05}"


def create_storage_account(
    account_credentials: dict, deployment_name: str, account_name_prefix: str, location: str
) -> DeploymentResponse:
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

        return DeploymentResponse(status="Success", response=account_name, note="Deployment Successful")
    except AzureError as azure_error:
        return DeploymentResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        return DeploymentResponse(status="Fail", note=str(exception))


if __name__ == "__main__":
    AZURE_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")
    AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID")
    AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
    OWNER = os.environ.get("OWNER")
    PURPOSE = os.environ.get("PURPOSE")

    if not OWNER or not PURPOSE:
        print("Please set the OWNER and PURPOSE environment variables")
        exit(0)
    deployment_id = OWNER + "-" + str(uuid.uuid1()) + "-" + PURPOSE

    # Authenticate the azure credentials
    account_credentials = sailazure.authenticate(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID
    )
    # Deploy Storage Account
    storage_account = create_storage_account(account_credentials, deployment_id, "stanaccountname", "westus")

    # Deploy the API services
    platform_services_ip = deploy_apiservices(account_credentials, deployment_id, OWNER, AZURE_SUBSCRIPTION_ID)
    print("API Services server: ", platform_services_ip)
    # Deploy the frontend server
    frontend_ip = deploy_frontend(account_credentials, deployment_id, platform_services_ip, AZURE_SUBSCRIPTION_ID)
    print("Frontend server: ", frontend_ip)

    print("\n\n===============================================================")
    print("Deployment complete. Please visit the link to access the demo: https://" + frontend_ip)
    print("SAIL API Services is hosted on: https://" + platform_services_ip + ":8000")

    print("Deployment ID: ", deployment_id)
    print("Kindly delete all the resource group created on azure with the deployment ID.")
    print("===============================================================\n\n")

    # # TODO: Prawal re-enable this once the orchestrator package is ready
    # Deploy the orchestro server
    # orchestrator_ip = deploy_orchestrator(account_credentials, deployment_id, "orchestrator")
    # print("Orchestrator IP: ", orchestrator_ip)

    # Delete the resource group for the backend server
    # sailazure.delete_resouce_group(account_credentials, deployment_id + "backend")
