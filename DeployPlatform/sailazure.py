from dataclasses import dataclass

from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import PublicIPAddress, PublicIPAddressSku
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode
from pydantic import BaseModel


@dataclass
class DeploymentInfo:
    credentials: ClientSecretCredential
    subscription_id: str
    object_id: str
    name: str
    id: str


class SailAzure:
    def set_deployment_info(self, deployment_info: DeploymentInfo):
        """Set the deployment information."""
        self.deployment_info = deployment_info

    def create_resource_group(self, resource_group_name, location):
        """Deploy the template to a resource group."""
        client = ResourceManagementClient(self.deployment_info.credentials, self.deployment_info.subscription_id)
        response = client.resource_groups.create_or_update(
            resource_group_name,
            {
                "location": location,
                "tags": {
                    "deployed_method": "DeployPlatform",
                },
            },  # type: ignore
        )
        assert response.properties is not None
        return response.properties.provisioning_state

    def authenticate(self, client_id, client_secret, tenant_id):
        """Authenticate using client_id and client_secret."""
        credentials = ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
        return credentials

    def deploy_template(self, resource_group_name, template, parameters):
        """Deploy the template to a resource group."""
        client = ResourceManagementClient(self.deployment_info.credentials, self.deployment_info.subscription_id)

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

        return deployment_async_operation.status()

    def delete_resouce_group(self, resource_group_name):
        """Deploy the template to a resource group."""
        client = ResourceManagementClient(self.deployment_info.credentials, self.deployment_info.subscription_id)
        delete_async_operation = client.resource_groups.begin_delete(resource_group_name)
        delete_async_operation.wait()

        print(delete_async_operation.status())

    def get_ip(self, resource_group_name, ip_resource_name):
        """Get the IP address of the resource."""
        client = NetworkManagementClient(self.deployment_info.credentials, self.deployment_info.subscription_id)
        public_ip_address = client.public_ip_addresses.get(resource_group_name, ip_resource_name)
        return public_ip_address.ip_address

    def get_private_ip(self, resource_group_name, network_interface_name) -> str:
        """Get the private IP of the virtual machine."""
        client = NetworkManagementClient(self.deployment_info.credentials, self.deployment_info.subscription_id)
        private_ip_address = client.network_interfaces.get(resource_group_name, network_interface_name)
        if private_ip_address.ip_configurations is None:
            raise Exception("No IP configuration found")

        if private_ip_address.ip_configurations[0].private_ip_address is None:
            raise Exception("No private IP address found")

        return private_ip_address.ip_configurations[0].private_ip_address

    def create_public_ip(self, resource_group_name, location, ip_resource_name) -> PublicIPAddress:
        client = NetworkManagementClient(self.deployment_info.credentials, "6e7f356c-6059-4799-b83a-c4744e4a7c2e")
        # Create Public ip resource
        params = PublicIPAddress(
            location=location,
            sku=PublicIPAddressSku(name="standard", tier="regional"),
            public_ip_allocation_method="static",
            public_ip_address_version="ipv4",
        )

        deployment_async_operation = client.public_ip_addresses.begin_create_or_update(
            resource_group_name, ip_resource_name, params
        )
        deployment_async_operation.wait()
        print(f"deployment_async_operation result:, {deployment_async_operation.result()}")
        print(f"IP creation status: {deployment_async_operation.status()}")

        return deployment_async_operation.result()

    def update_fw_pip(self, firewall_ip_id, firewall_ip_name):
        client = NetworkManagementClient(self.deployment_info.credentials, self.deployment_info.subscription_id)
        fw_info = client.azure_firewalls.get("rg-sail-wus-hub-001", "afw-sail-wus")
        fw_policy_info = client.firewall_policies.get("rg-sail-wus-hub-001", "afwpol-sail-wus-001")

        print(f"fw_info:\n {fw_info.as_dict()}\n")
        print(f"fw_info ip_configurations:\n {fw_info.ip_configurations}\n")
        print(f"fw_policy_info:\n {fw_policy_info.as_dict()}\n")
        print("\n\n===============================================================")
        # Update firewall with a specific new public ip address
        if fw_info.ip_configurations is None:
            fw_info.ip_configurations = []

        fw_info.ip_configurations.append(
            {
                "id": f"{firewall_ip_id}",
                "name": f"{firewall_ip_name}",
                "public_ip_address": {"id": f"{firewall_ip_id}"},
            }  # type: ignore
        )
        async_updated_fw_pip_result = client.azure_firewalls.begin_create_or_update(
            "rg-sail-wus-hub-001", "afw-sail-wus", fw_info
        ).result()
        print(async_updated_fw_pip_result)
        print("Updated a new Firewall Public ip to Firewall ip configuration")
        print("\n\n===============================================================")
        return async_updated_fw_pip_result, firewall_ip_name

    def update_nat_rule_policy(self, firewall_ip_name, firewall_ip, private_ip_address, port):
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
        self,
        firewall_ip_name,
        firewall_ip,
        private_ip_address,
        module_name,
    ):
        client = NetworkManagementClient(self.deployment_info.credentials, self.deployment_info.subscription_id)
        # Get current information on policies in rule collection groups
        fw_api_policy_rule_collection_info = client.firewall_policy_rule_collection_groups.get(
            "rg-sail-wus-hub-001",
            "afwpol-sail-wus-001",
            "APIRuleCollectionGroup",
        )

        # Update DNAT rule in Firewall for module
        if fw_api_policy_rule_collection_info.rule_collections is None:
            raise Exception("No rule collections found in APIRuleCollectionGroup")

        fw_api_policy_rule_collection_info.rule_collections[0].rules.append(
            self.update_nat_rule_policy(firewall_ip_name, firewall_ip, private_ip_address, "443")
        )

        async_updated_fw_pol_result = client.firewall_policy_rule_collection_groups.begin_create_or_update(
            "rg-sail-wus-hub-001",
            "afwpol-sail-wus-001",
            "APIRuleCollectionGroup",
            fw_api_policy_rule_collection_info,
        ).result()
        print(f"Updated a new Firewall DNAT RULE for {module_name}")
        return async_updated_fw_pol_result
