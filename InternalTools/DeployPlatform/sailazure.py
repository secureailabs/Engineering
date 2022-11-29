from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode


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
    public_ip_address = client.public_ip_addresses.get(resource_group_name, ip_resource_name)
    return public_ip_address.ip_address


def get_private_ip(accountCredentials, resource_group_name, network_interface_name):
    """Get the private IP of the virtual machine."""
    client = NetworkManagementClient(accountCredentials["credentials"], accountCredentials["subscription_id"])
    private_ip_address = client.network_interfaces.get(resource_group_name, network_interface_name)
    return private_ip_address.ip_configurations[0].private_ip_address


def create_public_ip(accountCredentials, resource_group_name, location, ip_resource_name):
    """
    Create public ip resource
    """
    client = NetworkManagementClient(accountCredentials["credentials"], accountCredentials["subscription_id"])
    # Create Public ip resource
    deployment_async_operation = client.public_ip_addresses.begin_create_or_update(
        resource_group_name,
        ip_resource_name,
        {
            "location": location,
            "sku": {"name": "standard", "tier": "regional"},
            "public_ip_allocation_method": "static",
            "public_ip_address_version": "ipv4",
        },
    )

    deployment_async_operation.wait()
    print(f"deployment_async_operation result:, {deployment_async_operation.result()}")
    print(f"IP creation status: {deployment_async_operation.status()}")
    public_ip_name = deployment_async_operation.result().name
    public_ip = deployment_async_operation.result().ip_address
    public_ip_id = deployment_async_operation.result().id

    return public_ip_name, public_ip, public_ip_id


def update_fw_pip(accountCredentials, firewall_ip_id, firewall_ip_name):
    """
    Update Firewall ip configuration with new public IP
    """
    client = NetworkManagementClient(accountCredentials["credentials"], accountCredentials["subscription_id"])
    fw_info = client.azure_firewalls.get("rg-sail-wus-hub-001", "afw-sail-wus")
    fw_policy_info = client.firewall_policies.get("rg-sail-wus-hub-001", "afwpol-sail-wus-001")

    print(f"fw_info:\n {fw_info.as_dict()}\n")
    print(f"fw_info ip_configurations:\n {fw_info.ip_configurations}\n")
    print(f"fw_policy_info:\n {fw_policy_info.as_dict()}\n")
    print("\n\n===============================================================")
    # Update firewall with a specific new public ip address
    fw_info.ip_configurations.append(
        {
            "id": f"{firewall_ip_id}",
            "name": f"{firewall_ip_name}",
            "public_ip_address": {"id": f"{firewall_ip_id}"},
        }
    )
    async_updated_fw_pip_result = client.azure_firewalls.begin_create_or_update(
        "rg-sail-wus-hub-001",
        "afw-sail-wus",
        fw_info,
    ).result()
    print(async_updated_fw_pip_result)
    print("Updated a new Firewall Public ip to Firewall ip configuration")
    print("\n\n===============================================================")
    return async_updated_fw_pip_result, firewall_ip_id, firewall_ip_name


def update_nat_rule_policy(firewall_ip_name, firewall_ip, private_ip_address, port):
    """
    Returns Dictionary of NAT Rule Policy

    :param firewall_ip_name: public IP for module
    :type firewall_ip_name: str
    :param firewall_ip: public IP for module
    :type firewall_ip: str
    :param private_ip_address: private IP for module
    :type private_ip_address: str
    :param port: Allowed port through firewall
    :type port: str
    :return: nat_rule_policy
    :rtype: dict
    """

    nat_rule_policy = {
        "name": f"{firewall_ip_name}_{port}",
        "rule_type": "NatRule",
        "ip_protocols": ["TCP"],
        "source_addresses": ["*"],
        "destination_addresses": [firewall_ip],
        "destination_ports": [port],
        "translated_address": private_ip_address,
        "translated_port": port,
        "source_ip_groups": [],
    }

    return nat_rule_policy


def update_fw_dnat_rules(
    accountCredentials,
    firewall_ip_name,
    firewall_ip,
    private_ip_address,
    module_name,
):
    """
    Update DNAT rules in Firewall for a specified Module

    :param accountCredentials: accountCredentials
    :type accountCredentials: accountCredentials
    :param firewall_ip_name: public IP for module
    :type firewall_ip_name: str
    :param firewall_ip: public IP for module
    :type firewall_ip: str
    :param private_ip_address: private IP for module
    :type private_ip_address: str
    :param module_name: module
    :type module_name: str
    :return:
    :rtype:
    """

    client = NetworkManagementClient(accountCredentials["credentials"], accountCredentials["subscription_id"])
    # Get current information on policies in rule collection groups
    fw_api_policy_rule_collection_info = client.firewall_policy_rule_collection_groups.get(
        "rg-sail-wus-hub-001",
        "afwpol-sail-wus-001",
        "APIRuleCollectionGroup",
    )
    fw_web_policy_rule_collection_info = client.firewall_policy_rule_collection_groups.get(
        "rg-sail-wus-hub-001",
        "afwpol-sail-wus-001",
        "WEBFRONTRuleCollectionGroup",
    )

    # Update DNAT rule in Firewall for module
    if module_name == "apiservices":
        fw_api_policy_rule_collection_info.rule_collections[0].rules.append(
            update_nat_rule_policy(firewall_ip_name, firewall_ip, private_ip_address, "8000")
        )
        async_updated_fw_pol_result = client.firewall_policy_rule_collection_groups.begin_create_or_update(
            "rg-sail-wus-hub-001",
            "afwpol-sail-wus-001",
            "APIRuleCollectionGroup",
            fw_api_policy_rule_collection_info,
        ).result()
    elif module_name == "newwebfrontend":
        fw_web_policy_rule_collection_info.rule_collections[0].rules.append(
            update_nat_rule_policy(firewall_ip_name, firewall_ip, private_ip_address, "443")
        )
        async_updated_fw_pol_result = client.firewall_policy_rule_collection_groups.begin_create_or_update(
            "rg-sail-wus-hub-001",
            "afwpol-sail-wus-001",
            "WEBFRONTRuleCollectionGroup",
            fw_web_policy_rule_collection_info,
        ).result()
    print(f"Updated a new Firewall DNAT RULE for {module_name}")
    return async_updated_fw_pol_result
