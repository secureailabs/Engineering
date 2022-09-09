import json
import os
import subprocess
import time
import uuid

import requests

import sailazure


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

    development_parameters = {
        "vmImageResourceId": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/"  # change this line depending on your subscription
        + "InitializerImageStorage-WUS-Rg/providers/Microsoft.Compute/images/"  # change this line depending on your subscription resourcegroup where images are stored
        + module_name,
        "virtualNetworkId": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/"  # change this line depending on your subscription
        + "rg-sail-wus-dev-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-dev-01",  # change this line depending on your vnet
        "subnetName": "snet-sail-wus-dev-platformservice-01",  # change this line depending on your vnet
    }

    release_candidate_parameters = {
        "vmImageResourceId": "/subscriptions/40cdb551-8a8d-401f-b884-db1599022002/resourceGroups/"  # change this line depending on your subscription
        + "InitializerImageStorage-WUS-Rg/providers/Microsoft.Compute/images/"  # change this line depending on your subscription resourcegroup where images are stored
        + module_name,
        "virtualNetworkId": "/subscriptions/40cdb551-8a8d-401f-b884-db1599022002/resourceGroups/"  # change this line depending on your subscription
        + "rg-sail-wus-rls-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-rls-01",  # change this line depending on your vnet
        "subnetName": "snet-sail-wus-rls-platformservice-01",  # change this line depending on your vnet
    }

    productionGA_parameters = {
        "vmImageResourceId": "/subscriptions/ba383264-b9d6-4dba-b71f-58b3755382d8/resourceGroups/"  # change this line depending on your subscription
        + "InitializerImageStorage-WUS-Rg/providers/Microsoft.Compute/images/"  # change this line depending on your subscription resourcegroup where images are stored
        + module_name,
        "virtualNetworkId": "/subscriptions/ba383264-b9d6-4dba-b71f-58b3755382d8/resourceGroups/"  # change this line depending on your subscription
        + "rg-sail-wus-prd-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-prd-01",  # change this line depending on your vnet
        "subnetName": "snet-sail-wus-prd-platformservice-01",  # change this line depending on your vnet
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

    deploy_status = sailazure.deploy_template(account_credentials, resource_group_name, template, parameters)
    print(module_name + " server status: ", deploy_status)

    virtual_machine_public_ip = sailazure.get_ip(account_credentials, resource_group_name, module_name + "-ip")

    return virtual_machine_public_ip


def deploy_apiservices(account_credentials, deployment_name, owner, subscription_id):
    # Deploy the frontend server
    apiservices_ip = deploy_module(account_credentials, deployment_name, "apiservices", subscription_id)

    # Read backend json from file
    with open("apiservices.json", "r") as backend_json_fd:
        backend_json = json.load(backend_json_fd)
    backend_json["owner"] = owner

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
