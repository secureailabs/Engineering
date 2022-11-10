from azure.mgmt.resource import ResourceManagementClient

from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode
from azure.identity import ClientSecretCredential


def create_resource_group(accountCredentials, resource_group_name, location):
    """Deploy the template to a resource group."""
    client = ResourceManagementClient(accountCredentials["credentials"], accountCredentials["subscription_id"])
    response = client.resource_groups.create_or_update(resource_group_name, {"location": location})
    return response.properties.provisioning_state


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
        resource_group_name, "azure-sample", {"properties": deployment_properties}
    )
    deployment_async_operation.wait()
    print("deployment_async_operation result ", deployment_async_operation.result())

    return deployment_async_operation.status()


def delete_resouce_group(accountCredentials, resource_group_name):
    """Deploy the template to a resource group."""
    client = ResourceManagementClient(accountCredentials["credentials"], accountCredentials["subscription_id"])
    delete_async_operation = client.resource_groups.begin_delete(resource_group_name)
    delete_async_operation.wait()

    print(delete_async_operation.status())


def get_ip(accountCredentials, resource_group_name, ip_resource_name):
    """Get the IP address of the resource."""
    client = NetworkManagementClient(accountCredentials["credentials"], accountCredentials["subscription_id"])
    foo = client.public_ip_addresses.get(resource_group_name, ip_resource_name)
    return foo.ip_address


def get_private_ip(accountCredentials, resource_group_name, network_interface_name):
    """Get the private IP of the virtual machine."""
    client = NetworkManagementClient(accountCredentials["credentials"], accountCredentials["subscription_id"])
    foo = client.network_interfaces.get(resource_group_name, network_interface_name)
    return foo.ip_configurations[0].private_ip_address
