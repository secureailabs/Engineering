# Readme

## Requirements
Have docker installed and docker service running. If not already done, install from https://secureailabs.atlassian.net/wiki/spaces/SAILConfluenceHome/pages/2153644033/Developer+Resources#Docker-installation

## Sail Platform Deployment Tool

The Azure VM Image Id is hard coded in the Engineering/InternalTools/DeployPlatform/Deploy.py. If the requirement is to use the new images the IDs need to change. This is a temporary file which will go away when the devops framework is mature enough to be used more easily than this script.

Setting the correct azure credential environment variables in the terminal:
```
export AZURE_SUBSCRIPTION_ID="3d2b9951-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export AZURE_TENANT_ID="3e74e5ef-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export AZURE_CLIENT_ID="4f909fab-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export AZURE_CLIENT_SECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
export AZURE_OBJECT_ID="5f6b5b5b-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```
Then run `sudo -E ./DeployPlatform.sh -p [Purpose:[Nightly, Bugfix, etc..]] -o [Owner: [Prawal, Stanley]]` from the root directory of the repository.
-E is needed to inherit the environment variables from the current user(non-root) shell.

## This script will
- Build and package all the relevant tools and packages.
- Create a backend virtual machine using the latest code and Initialization Vector in Docker/backend/InitializationVector.json
- Run DatabaseTools to populate the database on the server.
- Create a webfrontend virtual machine from the latest code with the initialization vector created at run time containing PlatformServicesUrl and VirtualMachinePublicIp which are the public IP address of the backend and the webfrontend VMs.

Note: The webfrontend takes some time to start up. So try connecting to it after 4-5 minutes the script ends.

## Cleanup
Delete the backend and webfrontend resource groups crated from the azure portal. The list of resource groups is listed after a successful run of the script.
This can also be done using a command like `az group delete --name <resource group name> --yes`.
