#!/bin/sh

ResourceGroup="VirtualMachineImageStorageRg"
StorageAccountName="sailcomputationimage9891"
Location="eastus"

PrintHelp()
{
    echo ""
    echo "Usage: $0 -m [Image Name]"
    echo "Usage: $0"
    echo -e "\t-m Module Name: backend | orchestrator | remotedataconnector | webfrontend | securecomputationnode"
    exit 1 # Exit script after printing help
}

# Parse the input parameters
while getopts "m:" opt
do
    echo "opt: $opt $OPTARG"
    case "$opt" in
        m ) imageName="$OPTARG" ;;
        ? ) PrintHelp ;;
    esac
done

# Check if the module name is provided
if [ -z "$imageName" ]
then
    echo "No module specified."
    exit 1
fi

# Check if packer is installed
packer --version
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Packer is not installed. Install it using and retry:"
    echo "curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -"
    echo "apt-add-repository \"deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main\""
    echo "apt-get update && apt-get install -y packer"
    exit $retVal
fi

# Check for Azure environment variables
if [ -z "${AZURE_SUBSCRIPTION_ID}" ]; then
  echo "environment variable AZURE_SUBSCRIPTION_ID is undefined"
  exit 1
fi
if [ -z "${AZURE_TENANT_ID}" ]; then
  echo "environment variable AZURE_TENANT_ID is undefined"
  exit 1
fi
if [ -z "${AZURE_CLIENT_ID}" ]; then
  echo "environment variable AZURE_CLIENT_ID is undefined"
  exit 1
fi
if [ -z "${AZURE_CLIENT_SECRET}" ]; then
  echo "environment variable AZURE_CLIENT_SECRET is undefined"
  exit 1
fi

# Create resource group for storage account
az group create \
--name $ResourceGroup \
--location $Location

# Create storage account
az storage account create \
--resource-group $ResourceGroup \
--name $StorageAccountName \
--location $Location \
--sku Standard_LRS \
--kind StorageV2 \
--access-tier Hot

# Ubuntu vhd Image
packer build \
-var location=$Location \
-var storage_resource_group=$ResourceGroup \
-var storage_account=$StorageAccountName \
-var module=$imageName \
packer-vhd-ubuntu.json

# TODO: Get the image id from packer output
# imageId=$(cat packer-manifest.json | grep "artifact_id" | awk '{print $2}')

# This is a manual step where the user needs to copy the url of generated vhd file to the storage account
read -p "Enter VHD image URL: " vhdImageUrl

# Create managed image from vhd
az image create \
--resource-group $ResourceGroup \
--name $imageName \
--source $vhdImageUrl \
--location $Location \
--os-type "Linux" \
--storage-sku "Standard_LRS"
