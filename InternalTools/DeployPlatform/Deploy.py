import json
import os
import subprocess
import time
import uuid

import sailazure


def deploy_module(account_credentials, deployment_name, module_name):
    """Deploy the template to a resource group."""
    print("Deploying module: ", module_name)

    # Each module will be deployed in a unique resource group
    resource_group_name = deployment_name + "-" + module_name

    # Create the resource group
    sailazure.create_resource_group(account_credentials, resource_group_name, "eastus")

    template_path = os.path.join(os.path.dirname(__file__), "ArmTemplates", module_name + ".json")

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
    deploy_status = sailazure.deploy_template(account_credentials, resource_group_name, template, parameters)
    print(module_name + " server status: ", deploy_status)

    virtual_machine_public_ip = sailazure.get_ip(account_credentials, resource_group_name, module_name + "-ip")

    return virtual_machine_public_ip


def deploy_apiservices(account_credentials, deployment_name, owner):
    # Deploy the frontend server
    apiservices_ip = deploy_module(account_credentials, deployment_name, "apiservices")

    # Read backend json from file
    # with open("apiservices.json", "r") as backend_json_fd:
    #     backend_json = json.load(backend_json_fd)
    backend_json = {}
    backend_json["Owner"] = owner

    with open("apiservices.json", "w") as outfile:
        json.dump(backend_json, outfile)

    upload_status = subprocess.run(
        [
            "./UploadPackageAndInitializationVector",
            "--IpAddress=" + apiservices_ip,
            "--Package=apiservices.tar.gz",
            "--InitializationVector=apiservices.json",
        ],
        stdout=subprocess.PIPE,
    )
    print("Upload status: ", upload_status.stdout)

    # Sleeping for two minutes
    time.sleep(2 * 60)

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


def deploy_frontend(account_credentials, deployment_name, platform_services_ip):
    # Deploy the frontend server
    frontend_server_ip = deploy_module(account_credentials, deployment_name, "newwebfrontend")

    # Prepare the initialization vector for the frontend server
    initialization_vector = {
        "apiservicesUrl": "https://" + platform_services_ip + ":8000",
        "VirtualMachinePublicIp": "https://" + frontend_server_ip + ":3000",
    }

    with open("newwebfrontend.json", "w") as outfile:
        json.dump(initialization_vector, outfile)

    upload_status = subprocess.run(
        [
            "./UploadPackageAndInitializationVector",
            "--IpAddress=" + frontend_server_ip,
            "--Package=newwebfrontend.tar.gz",
            "--InitializationVector=newwebfrontend.json",
        ],
        stdout=subprocess.PIPE,
    )
    print("Upload status: ", upload_status.stdout)

    return frontend_server_ip


def deploy_orchestrator(account_credentials, deployment_name):
    # Deploy the orchestrator server
    orchestrator_server_ip = deploy_module(account_credentials, deployment_name, "orchestrator")

    # There is no initialization vector for the orchestrator
    initialization_vector = {"apiservicesUrl": "https://" + platform_services_ip + ":8000"}

    with open("orchestrator.json", "w") as outfile:
        json.dump(initialization_vector, outfile)

    upload_status = subprocess.run(
        [
            "./UploadPackageAndInitializationVector",
            "--IpAddress=" + orchestrator_server_ip,
            "--Package=orchestrator.tar.gz",
            "--InitializationVector=orchestrator.json",
        ],
        stdout=subprocess.PIPE,
    )
    print("Upload status: ", upload_status.stdout)

    return orchestrator_server_ip


if __name__ == "__main__":
    AZURE_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")
    AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID")
    AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
    OWNER = os.environ.get("OWNER")
    PURPOSE = os.environ.get("PURPOSE")

    deployment_id = OWNER + "-" + str(uuid.uuid1()) + "-" + PURPOSE

    # Authenticate the azure credentials
    account_credentials = sailazure.authenticate(
        AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID
    )

    # Deploy the platform services
    platform_services_ip = deploy_apiservices(account_credentials, deployment_id, OWNER)
    print("Platform Services server: ", platform_services_ip)

    # Deploy the frontend server
    frontend_ip = deploy_frontend(account_credentials, deployment_id, platform_services_ip)
    print("Frontend server: ", frontend_ip)

    print("\n\n===============================================================")
    print("Deployment complete. Please visit the link to access the demo: https://" + frontend_ip + ":3000")
    print("SAIL Platorm Services is hosted on: https://" + platform_services_ip + ":8000")
    print("Deployment ID: ", deployment_id)
    print("Kindly delete all the resource group created on azure with the deployment ID.")
    print("===============================================================\n\n")

    # TODO: Prawal re-enable this once the orchestrator package is ready
    # Deploy the orchestro server
    # orchestrator_ip = deploy_orchestrator(account_credentials, deployment_id, "orchestrator")
    # print("Orchestrator IP: ", orchestrator_ip)

    # Delete the resource group for the backend server
    # sailazure.delete_resouce_group(account_credentials, deployment_id + "backend")
