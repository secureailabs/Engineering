#!/bin/bash

# Remember to decrypt .env.dev.encrypted with 'npm run env:decrypt'
source .env.dev
Location="westus"

PrintHelp()
{
    echo ""
    echo "Usage: $0 -m [Image Name] [-a]"
    echo "Usage: $0"
    echo -e "\t-m Module Name: apiservices | newwebfrontend | rpcrelated | smartbroker"
    echo -e "\t-a ci_flag will be set to true"
    exit 1 # Exit script after printing help
}

# Parse the input parameters
while getopts "m:a" opt
do
    echo "opt: $opt $OPTARG"
    case "$opt" in
        a ) ci_flag="yes" ;;
        m ) imageName="$OPTARG" ;;
        ? ) PrintHelp ;;
    esac
done

# Check if the module name is provided
if [ -z "$imageName" ]; then
    echo "No module specified."
    exit 1
fi

# Define the path for the module, default path is the Docker folder in the engineering repo
dockerDir=$(realpath ../..)

# The smartbroker module is in a the datascience folder under Engineering
if [ "$imageName" == "smartbroker" ]; then
    dockerDir=$(realpath ../../datascience)
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

if [ -z "$ci_flag" ]; then
    # Bash Menu
    # TODO Technially all subscriptions for this script can share 1 SP: Discussion We should create singular SP for PACKER
    echo -e "\nPlease Specify # for targeted subscription to upload image: "
    options=("Development" "Release Candidate" "ProductionGA" "Quit")
    select opt in "${options[@]}"
    do
        case $REPLY in
            1)
                echo -e "\n==== Setting env variables for $opt ===="
                export AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID
                ResourceGroup=$DEVELOPMENT_RESOURCE_GROUP # This needs to get updated per choice of subscription
                imageGalleryName=$DEVELOPMENT_IMAGE_GALLERY_NAME # This needs to get updated per choice of subscription
                break
                ;;
            2)
                echo -e "\n==== Setting env variables for $opt ===="
                export AZURE_SUBSCRIPTION_ID=$RELEASE_CANDIDATE_SUBSCRIPTION_ID
                ResourceGroup=$RELEASE_CANDIDATE_RESOURCE_GROUP # This needs to get updated per choice of subscription
                imageGalleryName=$RELEASE_CANDIDATE_IMAGE_GALLERY_NAME # This needs to get updated per choice of subscription
                break
                ;;
            3)
                echo -e "\n==== Setting env variables for $opt ===="
                export AZURE_SUBSCRIPTION_ID=$PRODUCTION_GA_SUBSCRIPTION_ID
                ResourceGroup=$PRODUCTION_GA_RESOURCE_GROUP # This needs to get updated per choice of subscription
                imageGalleryName=$PRODUCTION_GA_IMAGE_GALLERY_NAME # This needs to get updated per choice of subscription
                break
                ;;
            4)
                exit 0
                ;;
        esac
    done
fi

# Set the subscription
echo -e "==== Login to Azure and Set Subscription ====\n"
az login --service-principal --username $AZURE_CLIENT_ID --password $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
az account set --subscription $AZURE_SUBSCRIPTION_ID
echo -e "\n==== Verify Subscription Set Properly ====\n"
az account show

# list custom SAIL managed images
echo -e "\n==== Azure Image List ====\n"
output=$(az image list \
--resource-group $ResourceGroup)
echo "$output"

# Delete old custom SAIL managed images
echo -e "\n==== Azure Image Delete As Required ====\n"
az image delete \
--resource-group $ResourceGroup \
--name $imageName
echo "Deletion Completed, continuing..."

echo -e "\n==== Azure VHD& Image Creation Begins ====\n"
# Create resource group for storage account
az group create \
--name $ResourceGroup \
--location $Location

# Create the shared image gallery
az sig create \
--resource-group $ResourceGroup \
--gallery-name $imageGalleryName \
--location $Location

# Create the image definition
az sig image-definition create \
--resource-group $ResourceGroup \
--gallery-name $imageGalleryName \
--gallery-image-definition $imageName \
--features SecurityType=ConfidentialVMSupported \
--publisher "SAIL" \
--hyper-v-generation V2 \
--offer $imageName \
--sku "Standard_LRS" \
--os-type "Linux"

# Ubuntu vhd Image
packer build \
-var location=$Location \
-var resource_group_name=$ResourceGroup \
-var module=$imageName \
-var docker_dir=$dockerDir \
-var gallery_name=$imageGalleryName \
packer-vhd-ubuntu.json
