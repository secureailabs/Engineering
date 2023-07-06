import json
import os
import random
import time
import uuid

import yaml
from azure.core.exceptions import AzureError
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.models import DiagnosticSettingsResource, LogSettings, MetricSettings
from azure.mgmt.network.models import PublicIPAddress
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountListKeysResult
from azure.storage.blob import BlobServiceClient
from database_initialization import initialize_database
from pydantic import BaseModel, Field, StrictStr
from sail_dns_management_client import Client as DNSClient
from sail_dns_management_client.api.default import add_domain_dns_post
from sail_dns_management_client.models import DomainData
from sailazure import DeploymentInfo, SailAzure

AZURE_SUBSCRIPTION_ID = os.environ["AZURE_SUBSCRIPTION_ID"]
AZURE_TENANT_ID = os.environ["AZURE_TENANT_ID"]
AZURE_CLIENT_ID = os.environ["AZURE_CLIENT_ID"]
AZURE_OBJECT_ID = os.environ["AZURE_OBJECT_ID"]
AZURE_CLIENT_SECRET = os.environ["AZURE_CLIENT_SECRET"]
OWNER = os.environ["OWNER"]
PURPOSE = os.environ["PURPOSE"]
VERSION = os.environ["VERSION"]
DOCKER_REGISTRY_URL = os.environ["DOCKER_REGISTRY_URL"]
DOCKER_REGISTRY_USERNAME = os.environ["DOCKER_REGISTRY_USERNAME"]
DOCKER_REGISTRY_PASSWORD = os.environ["DOCKER_REGISTRY_PASSWORD"]
API_SERVICES_TAG = os.environ["API_SERVICES_TAG"]
AUDIT_SERVICES_TAG = os.environ["AUDIT_SERVICES_TAG"]
SCN_TAG = os.environ["SCN_TAG"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
DATA_UPLOAD_TAG = os.environ["DATA_UPLOAD_TAG"]
USER_PORTAL_TAG = os.environ["USER_PORTAL_TAG"]
GATEWAY_TAG = os.environ["GATEWAY_TAG"]
LOCATION = "westus"

BASE_DOMAIN = os.environ["BASE_DOMAIN"]
API_SERVICE_URL = f"https://api.{BASE_DOMAIN}"
AUDIT_SERVICE_URL = f"https://audit.{BASE_DOMAIN}"
DATA_UPLOAD_URL = f"https://dataupload.{BASE_DOMAIN}"
USER_PORTAL_URL = f"https://userportal.{BASE_DOMAIN}"

DEV_PARAMS = {
    "azure_subscription_id": "b7a46052-b7b1-433e-9147-56efbfe28ac5",
    "vmImageResourceId": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/SAIL-PAYLOADS-ImageStorage-WUS-CVM-Rg/providers/Microsoft.Compute/galleries/sail_image_gallery/images/sailbaseimage/versions/0.1.0",
    "virtualNetworkId": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/rg-sail-wus-dev-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-dev-01",
    "subnetName": "snet-sail-wus-dev-platformservice-01",
    "subnet_id": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/rg-sail-wus-dev-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-dev-01/subnets/snet-sail-wus-dev-platformservice-01",
    "azure_scn_subnet_name": "snet-sail-wus-dev-scn-01",
    "azure_storage_resource_group": "SAIL-PAYLOADS-ImageStorage-WUS-Rg",
    "azure_storage_account_name": "sailvmimages9827",
    "azure_scn_virtual_network_id": "/subscriptions/b7a46052-b7b1-433e-9147-56efbfe28ac5/resourceGroups/rg-sail-wus-dev-vnet-01/providers/Microsoft.Network/virtualNetworks/vnet-sail-wus-dev-01",
    "vmSize": "Standard_D4s_v4",
    "adminUserName": "sailuser",
    "adminPassword": "SailPassword@123",
}


class DeploymentResponse(BaseModel):
    status: StrictStr = Field(...)
    response: StrictStr = Field(default="")
    ip_address: StrictStr = Field(default="")
    note: StrictStr = Field(...)


sailazure = SailAzure()

deployment_id = str(uuid.uuid1())
DEPLOYMENT_INFO = DeploymentInfo(
    credentials=sailazure.authenticate(AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID),
    object_id=AZURE_OBJECT_ID,
    subscription_id=AZURE_SUBSCRIPTION_ID,
    id=deployment_id,
    name=f"{OWNER}-{deployment_id}-{PURPOSE}",
    location=LOCATION,
)
sailazure.set_deployment_info(DEPLOYMENT_INFO)


def deploy_module(module_name, custom_data) -> str:

    # Deploy the template to a resource group.
    print("Deploying module: ", module_name)

    # Each module will be deployed in a unique resource group
    resource_group_name = DEPLOYMENT_INFO.name + "-" + module_name

    # Create the resource group
    sailazure.create_resource_group(resource_group_name)

    template_path = os.path.join(os.path.dirname(__file__), "ArmTemplates", "sailvm.json")

    with open(template_path, "r") as template_file_fd:
        template = json.load(template_file_fd)

    parameters = {
        "vmName": module_name,
        "vmSize": DEV_PARAMS["vmSize"],
        "adminUserName": DEV_PARAMS["adminUserName"],
        "adminPassword": DEV_PARAMS["adminPassword"],
        "vmImageResourceId": DEV_PARAMS["vmImageResourceId"],
        "subnetName": DEV_PARAMS["subnetName"],
        "virtualNetworkId": DEV_PARAMS["virtualNetworkId"],
        "customData": custom_data,
    }

    deploy_status = sailazure.deploy_template(resource_group_name, template, parameters)
    print(f"{module_name} server status: {deploy_status}")

    # virtual_machine_public_ip = sailazure.get_ip( resource_group_name, module_name + "-ip")
    virtual_machine_private_ip = sailazure.get_private_ip(resource_group_name, module_name + "-nic")

    return virtual_machine_private_ip


def get_randomized_name(prefix: str) -> str:
    return f"{prefix}{random.randint(1,100000):05}"


def deploy_key_vault(key_vault_name_prefix, storage_account_id):
    # Key vault will be deployed in a unique resource group
    resource_group_name = DEPLOYMENT_INFO.name + "-keyvault"

    # Create a key vault name that's available because they're used in URLs.
    keyvault_client = KeyVaultManagementClient(
        credential=DEPLOYMENT_INFO.credentials, subscription_id=DEPLOYMENT_INFO.subscription_id
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
    sailazure.create_resource_group(resource_group_name)

    template_path = os.path.join(os.path.dirname(__file__), "ArmTemplates", "keyvault" + ".json")

    with open(template_path, "r") as template_file_fd:
        template = json.load(template_file_fd)

    parameters = {
        "keyvault_name": key_vault_name,
        "azure_tenant_id": DEPLOYMENT_INFO.credentials._tenant_id,
        "azure_object_id": DEPLOYMENT_INFO.object_id,
    }

    deploy_status = sailazure.deploy_template(resource_group_name, template, parameters)
    print("keyvault status: ", deploy_status)

    if deploy_status != "Succeeded":
        raise Exception("Keyvault deployment failed")

    keyvault_url = f"https://{key_vault_name}.vault.azure.net/"

    # Setup monitoring and audit logs
    key_vault_resource_id = f"/subscriptions/{DEPLOYMENT_INFO.subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.KeyVault/vaults/{key_vault_name}"
    monitor_client = MonitorManagementClient(
        credential=DEPLOYMENT_INFO.credentials, subscription_id=DEPLOYMENT_INFO.subscription_id
    )

    diagnostic_settings_resource = DiagnosticSettingsResource(
        storage_account_id=storage_account_id,
        logs=[LogSettings(category="AuditEvent", enabled=True)],
        metrics=[MetricSettings(category="AllMetrics", enabled=True)],
    )

    monitor_client.diagnostic_settings.create_or_update(
        resource_uri=key_vault_resource_id,
        name="Key vault logs",
        parameters=diagnostic_settings_resource,  # type: ignore
    )

    # return the url of the keyvault
    return keyvault_url


def create_cloud_init_file(
    initialization_json: dict, imageName: str, docker_params: str, image_tag: str, run_image: bool = True
):
    """Create the cloud init file"""
    cloud_init_file = "#cloud-config\n"

    cloud_init_yaml = {}

    # Copy the initialization.json file to the VM
    cloud_init_yaml["write_files"] = [
        {
            "path": "/etc/initialization.json",
            "content": json.dumps(initialization_json, indent=4),
        }
    ]

    cloud_init_yaml["runcmd"] = [
        f"sudo mkdir -p /opt/{imageName}_dir",
        f"sudo docker login {DOCKER_REGISTRY_URL} --username {DOCKER_REGISTRY_USERNAME} --password {DOCKER_REGISTRY_PASSWORD}",
    ]

    if run_image:
        cloud_init_yaml["runcmd"].append(
            f"sudo docker run -dit {docker_params} --name {imageName} {DOCKER_REGISTRY_URL}/{imageName}:{image_tag}",
        )

    cloud_init_file += yaml.dump(cloud_init_yaml)

    return cloud_init_file


def deploy_audit_service(storage_account_name):
    # Read backend json from file and set params
    audit_json = {}
    audit_json["owner"] = OWNER
    audit_json["azure_storage_account_name"] = storage_account_name
    audit_json["azure_tenant_id"] = DEPLOYMENT_INFO.credentials._tenant_id
    audit_json["azure_client_id"] = DEPLOYMENT_INFO.credentials._client_id
    audit_json["azure_client_secret"] = DEPLOYMENT_INFO.credentials._client_credential

    with open("auditserver.json", "w") as outfile:
        json.dump(audit_json, outfile)

    # Create a cloud-init file
    custom_data = create_cloud_init_file(
        audit_json,
        "auditserver",
        "-v /etc/initialization.json:/app/InitializationVector.json -p 3100:3100",
        AUDIT_SERVICES_TAG,
    )

    # Deploy the frontend server
    audit_service_ip = deploy_module("auditserver", custom_data)

    return audit_service_ip


def deploy_apiservices(
    storage_account_name, storage_account_password, storage_resource_group_name, key_vault_url, gateway_ip
) -> str:
    # Read backend json from file and set params
    backend_json = {}
    backend_json["jwt_secret"] = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    backend_json["refresh_secret"] = "52bb444a1aabb9a76792527e6605349e1cbc7fafb8624de4e0ddde4f84ad4066"
    backend_json["password_pepper"] = "06ac6368872b368a8c67e41c1a8faa46e8471818cdbb442345fbb2205b9fc225"
    backend_json["sail_email"] = "no-reply@secureailabs.com"
    backend_json["sail_password"] = "password"
    backend_json["azure_scn_user_name"] = "sailuser"
    backend_json["azure_scn_password"] = "SailPassword@123"
    backend_json["owner"] = OWNER
    backend_json["azure_subscription_id"] = DEPLOYMENT_INFO.subscription_id
    backend_json["azure_tenant_id"] = DEPLOYMENT_INFO.credentials._tenant_id
    backend_json["azure_client_id"] = DEPLOYMENT_INFO.credentials._client_id
    backend_json["azure_client_secret"] = DEPLOYMENT_INFO.credentials._client_credential
    backend_json["azure_scn_image_id"] = DEV_PARAMS["vmImageResourceId"]
    backend_json["azure_scn_subnet_name"] = DEV_PARAMS["azure_scn_subnet_name"]
    backend_json["azure_storage_resource_group"] = storage_resource_group_name
    backend_json["azure_storage_account_name"] = storage_account_name
    backend_json["azure_scn_virtual_network_id"] = DEV_PARAMS["azure_scn_virtual_network_id"]
    backend_json["azure_storage_account_password"] = storage_account_password
    backend_json["azure_keyvault_url"] = key_vault_url
    backend_json["version"] = VERSION
    backend_json["audit_service_ip"] = audit_service_ip
    backend_json["slack_webhook"] = SLACK_WEBHOOK_URL
    backend_json["docker_registry_url"] = DOCKER_REGISTRY_URL
    backend_json["docker_registry_username"] = DOCKER_REGISTRY_USERNAME
    backend_json["docker_registry_password"] = DOCKER_REGISTRY_PASSWORD
    backend_json[
        "securecomputationnode_docker_params"
    ] = "-p 8000:8888 --cap-add=SYS_ADMIN --cap-add=DAC_READ_SEARCH --privileged"
    backend_json["securecomputationnode_image_tag"] = SCN_TAG
    backend_json["base_domain"] = BASE_DOMAIN
    backend_json["dns_ip"] = gateway_ip

    # Create a cloud-init file
    custom_data = create_cloud_init_file(
        backend_json,
        "apiservices",
        "-v /etc/initialization.json:/InitializationVector.json -p 8000:8000",
        API_SERVICES_TAG,
    )

    # Deploy the apiservices server
    apiservices_ip = deploy_module("apiservices", custom_data)

    # Sleeping for some time
    time.sleep(120)

    # Run database tools for the backend server
    initialize_database(hostname=f"http://{apiservices_ip}:8000")
    print("Api Services Database Initialization Tool run: Success")

    return apiservices_ip


def deploy_dataupload_service():
    # Create a cloud-init file
    custom_data = create_cloud_init_file(
        {}, "dataupload", f"-p 8000:8000 --env SAIL_API_SERVICE_URL={API_SERVICE_URL}", DATA_UPLOAD_TAG
    )

    # Deploy the apiservices server
    data_upload_ip = deploy_module("dataupload", custom_data)

    return data_upload_ip


def deploy_user_portal():
    # Create a cloud-init file
    custom_data = create_cloud_init_file(
        {},
        "userportal",
        f"-p 8000:3000 --env REACT_APP_SAIL_API_SERVICE_URL={API_SERVICE_URL} --env REACT_APP_SAIL_DATA_UPLOAD_SERVICE_URL={DATA_UPLOAD_URL}",
        USER_PORTAL_TAG,
    )

    # Deploy the apiservices server
    data_upload_ip = deploy_module("userportal", custom_data)

    return data_upload_ip


def deploy_gateway(public_ip: bool):

    gateway_iv = {}
    gateway_iv["root_domain"] = BASE_DOMAIN

    # Create a cloud-init file
    custom_data = create_cloud_init_file(
        gateway_iv,
        "gateway",
        f"-p 443:443 -p 8000:8001 -v /etc/initialization.json:/InitializationVector.json -v /opt/certs/nginx-selfsigned.crt:/etc/nginx/certs/fullchain.pem -v /opt/certs/nginx-selfsigned.key:/etc/nginx/certs/privkey.pem",
        GATEWAY_TAG,
        False,
    )

    # Deploy the gateway server
    gateway_ip = deploy_module("gateway", custom_data)

    return gateway_ip


def create_storage_account(account_name_prefix: str):
    try:
        # Provision the storage account, starting with a management object.
        storage_client = StorageManagementClient(DEPLOYMENT_INFO.credentials, DEPLOYMENT_INFO.subscription_id)

        # Each module will be deployed in a unique resource group
        resource_group_name = DEPLOYMENT_INFO.name + "-storage"

        # Create the resource group
        sailazure.create_resource_group(resource_group_name)

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
            {"location": DEPLOYMENT_INFO.location, "kind": "StorageV2", "sku": {"name": "Standard_LRS"}},  # type: ignore
        )
        # Long-running operations return a poller object; calling poller.result() waits for completion.
        account_result = poller.result()

        # Get the storage account key
        keys: StorageAccountListKeysResult = storage_client.storage_accounts.list_keys(resource_group_name, account_name)  # type: ignore
        storage_account_key: str = keys.keys[0].value  # type: ignore

        # Create container
        az_oauth_url = f"https://{account_name}.blob.core.windows.net"
        blob_service_client = BlobServiceClient(account_url=az_oauth_url, credential=DEPLOYMENT_INFO.credentials)
        container_client = blob_service_client.get_container_client("audit")
        container_client.create_container()

        return (
            DeploymentResponse(status="Success", response=account_name, note="Deployment Successful"),
            account_name,
            storage_account_key,
            resource_group_name,
        )
    except AzureError as azure_error:
        print(str(azure_error))
        return DeploymentResponse(status="Fail", note=str(azure_error))
    except Exception as exception:
        print(str(exception))
        return DeploymentResponse(status="Fail", note=str(exception))


def update_firewall(private_ip_address: str, firewall_ip: PublicIPAddress):
    sailazure.update_fw_pip(firewall_ip)

    if firewall_ip.name is None or firewall_ip.ip_address is None:
        raise Exception("Firewall Public IP Address is not available")

    # Update DNAT Rules per module
    sailazure.update_fw_dnat_rules(firewall_ip, private_ip_address)


if __name__ == "__main__":
    # Check if public ip is required
    public_ip = False
    if "PUBLIC_IP" in os.environ:
        public_ip = os.getenv("PUBLIC_IP", "False") == "True"

    if not OWNER or not PURPOSE:
        print("Please set the OWNER and PURPOSE environment variables")
        exit(1)

    # Deploy Storage Account
    (
        storage_account,
        storage_account_name,
        storage_accout_password,
        storage_resource_group_name,
    ) = create_storage_account("saildatastorage")

    # Create storage account id
    storage_account_id = f"/subscriptions/{AZURE_SUBSCRIPTION_ID}/resourceGroups/{storage_resource_group_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}"

    # Provision a key vault
    key_vault_url = deploy_key_vault(key_vault_name_prefix="sailkeyvault", storage_account_id=storage_account_id)

    # Deploy the audit services
    audit_service_ip = deploy_audit_service(storage_account_name)
    print("Audit Service server: ", audit_service_ip)

    # Deploy the Gateway
    gateway_private_ip = deploy_gateway(public_ip)
    print("Gateway server: ", gateway_private_ip)

    # Ask the user if they want to add a DNS mapping to the gateway
    if public_ip:
        # Authenticate the azure credentials for SAIL GLOBAL HUB
        DEPLOYMENT_INFO.subscription_id = "6e7f356c-6059-4799-b83a-c4744e4a7c2e"
        sailazure.set_deployment_info(DEPLOYMENT_INFO)

        pip_name = "PIP-" + deployment_id + "-gateway"
        public_ip = sailazure.create_public_ip("rg-sail-wus-hubpipdev-001", pip_name)
        if public_ip.id is None or public_ip.name is None or public_ip.ip_address is None:
            raise Exception("Unable to create public ip address")
        update_firewall(gateway_private_ip, public_ip)

        # Revert the azure credentials back to the user's subscription
        DEPLOYMENT_INFO.subscription_id = AZURE_SUBSCRIPTION_ID
        sailazure.set_deployment_info(DEPLOYMENT_INFO)
        pass
    else:
        print("Continuing without public ip and using the private ip for the gateway")
        # TODO: Add a private DNS to the gateway
        pass

    # Ask the user to add the SSL certificates to the gateway and then type done to continue
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Please add the SSL certificates to the gateway and type 'done' to continue")
    print("Instructions:")
    print("1. SSH to the gateway VM using the following command:")
    print(f"ssh sailuser@{gateway_private_ip}")
    print("2. Create ssl certificates by following the instructions on executing:")
    print("sudo su")
    print(
        f"docker run -it --rm --name certbot -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt certbot/certbot certonly --manual --preferred-challenges dns -d *.{BASE_DOMAIN}"
    )
    print("3. Start the gateway nginx server:")
    print(
        f"docker run -dit -p 443:443 -p 8000:8001 -v /etc/letsencrypt:/etc/letsencrypt -v /etc/initialization.json:/InitializationVector.json --name gateway {DOCKER_REGISTRY_URL}/gateway:{GATEWAY_TAG}"
    )
    print("4. Exit the VM by typing 'exit'")

    # Continue only if the user types done
    while True:
        user_input = input("Please add the SSL certificates to the gateway and type 'done' to continue: ")
        if user_input.lower() == "done":
            break

    # Create the dns client
    dns_client = DNSClient(
        base_url=f"https://{gateway_private_ip}:8000",
        verify_ssl=False,
        raise_on_unexpected_status=True,
        timeout=30,
        follow_redirects=True,
    )

    # Deploy the API services
    api_services_ip = deploy_apiservices(
        storage_account_name, storage_accout_password, storage_resource_group_name, key_vault_url, gateway_private_ip
    )
    print("API Services server: ", api_services_ip)
    request = DomainData(ip=api_services_ip, domain=f"api.{BASE_DOMAIN}.")
    add_domain_dns_post.sync(client=dns_client, json_body=request)

    # Deploy the data upload service
    data_upload_service_ip = deploy_dataupload_service()
    print("Data Upload Service server: ", data_upload_service_ip)
    request = DomainData(ip=data_upload_service_ip, domain=f"dataupload.{BASE_DOMAIN}.")
    add_domain_dns_post.sync(client=dns_client, json_body=request)

    # Deploy the user portal
    user_portal_ip = deploy_user_portal()
    print("User Portal server: ", user_portal_ip)
    request = DomainData(ip=user_portal_ip, domain=f"userportal.{BASE_DOMAIN}.")
    add_domain_dns_post.sync(client=dns_client, json_body=request)

    print("\n\n===============================================================")
    print("================= SUMMARY: Deploy Platform =====================")
    print(f"SAIL platform is hosted on: https://{BASE_DOMAIN}")
    print(f"Deployment ID: {deployment_id}")
    print("Kindly delete all the resource group created on azure with the deployment ID.")
    print("===============================================================\n\n")

    # Delete the resource group for the backend server
    # sailazure.delete_resouce_group( deployment_id + "backend")
