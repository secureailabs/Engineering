# Readme

## Sail Platform Deployment Tool

The Azure VM Image Id is hard coded in the Engineering/Milestone5/InternalTools/DeployPlatform/Deploy.py. If the requirement is to use the new images the IDs need to change. This is a temporary file which will go away when the devops framework is mature enough to be used more easily than this script.

Setting the correct azure credential environment variables in the terminal:
```
export AZURE_SUBSCRIPTION_ID="3d2b9951-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export AZURE_TENANT_ID="3e74e5ef-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export AZURE_CLIENT_ID="4f909fab-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export AZURE_CLIENT_SECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```
Then run `sudo ./DeployPlatform.sh` from the root directory of the repository.

This script will:
- Build and package all the relevant tools and packages.
- Create a backend virtual machine using the latest code and Initialization Vector in Docker/backend/InitializationVector.json
- Run DatabaseTools to populate the database on the server.
- Create a webfrontend virtual machine from the latest code with the initialization vector created at run time containing PlatformServicesUrl and VirtualMachinePublicIp which are the public IP address of the backend and the webfrontend VMs.
