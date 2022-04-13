# Managed Images using Packer

## Install Packer
```
curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -
apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
apt-get update && apt-get install -y packer
```
## Set the Azure login credentials
Azure credentials are provided as environment variables.
```
export AZURE_SUBSCRIPTION_ID="xxxx-xxxx-xxxx-xxxx-xxxx-xxxx-xxxx"
export AZURE_TENANT_ID="xxxx-xxxx-xxxx-xxxx-xxxx-xxxx-xxxx"
export AZURE_CLIENT_ID="xxxx-xxxx-xxxx-xxxx-xxxx-xxxx-xxxx"
export AZURE_CLIENT_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## Run image create script
Run the AzureImageCreate.sh script to build VM images which is a two step process.
First it will create a VHD image using packer and then there is a manual process to convert that image to a managed image.
where the user needs to copy the vhd image url and paste it as a user input in the terminal when asked for.

## Requirements
`../../Binary/BaseVmImageInit` should exist before running this script.
Both can be created by running `make all` in the `VirtualMachine/BaseVmImageInit` directory.
