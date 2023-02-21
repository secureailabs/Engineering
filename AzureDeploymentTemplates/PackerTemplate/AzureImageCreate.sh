#!/bin/bash

source azure_constants.sh

# Get the version from the VERSION file
ImageVersion=$(cat ../../VERSION)
ImageName="sailbaseimage"

PrintHelp()
{
    echo ""
    echo "Usage: $0 [-a]"
    echo "Usage: $0"
    echo -e "\t-a ci_flag will be set to true"
    exit 1 # Exit script after printing help
}

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

# Check if the AZURE_SUBSCRIPTION_ID is set
if [ -z $AZURE_SUBSCRIPTION_ID ]; then
    echo "AZURE_SUBSCRIPTION_ID is not set. Set it and retry."
    exit 1
fi

# Set the subscription
echo -e "==== Login to Azure and Set Subscription ====\n"
az login --service-principal --username $AZURE_CLIENT_ID --password $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
az account set --subscription $AZURE_SUBSCRIPTION_ID
az account show

# list custom SAIL managed images
echo -e "\n==== Azure Image List ====\n"
az image list \
--resource-group $RESOURCE_GROUP

# Delete old custom SAIL managed images
echo -e "\n==== Azure Image Delete As Required ====\n"
az image delete \
--resource-group $RESOURCE_GROUP \
--name $ImageName

az sig image-version delete \
--gallery-image-version $ImageVersion \
--gallery-image-definition $ImageName \
--gallery-name $IMAGE_GALLERY_NAME \
--resource-group $RESOURCE_GROUP
echo "Image Version Deletion Completed, continuing..."

# Create resource group for storage account
echo -e "\n==== Azure Managed Image Creation Begins ====\n"
az group create \
--name $RESOURCE_GROUP \
--location $LOCATION

# Create the shared image gallery
az sig create \
--resource-group $RESOURCE_GROUP \
--gallery-name $IMAGE_GALLERY_NAME \
--location $LOCATION

# Create the image definition
az sig image-definition create \
--resource-group $RESOURCE_GROUP \
--gallery-name $IMAGE_GALLERY_NAME \
--gallery-image-definition $ImageName \
--features SecurityType=ConfidentialVMSupported \
--publisher "Secure-AI-Labs" \
--hyper-v-generation V2 \
--offer $ImageName \
--sku "sail" \
--os-type "Linux"

# Get the short git commit hash
gitCommitHash=$(git rev-parse --short HEAD)

# Ubuntu Image in shared image gallery
packer build \
-var location="$LOCATION" \
-var resource_group_name="$RESOURCE_GROUP" \
-var module="$ImageName" \
-var gallery_name="$IMAGE_GALLERY_NAME" \
-var version="$ImageVersion" \
-var gitCommitHash="$gitCommitHash" \
packer-sig-ubuntu.json

# Tag the image with the short git commit hash
az image update \
--resource-group $RESOURCE_GROUP \
--name $ImageName \
--tags gitCommitHash=$gitCommitHash

# clean up the datascience moved to Docker/rpcrelated
echo "--------------------------------------------------"
echo "cleaning up"
echo "--------------------------------------------------"
(cd ../../ && make clean_datascience)
