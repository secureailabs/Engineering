#!/bin/bash

source azure_constants.sh
Location="westus"
ImageGalleryName="sail_image_gallery"

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
        m ) ImageName="$OPTARG" ;;
        ? ) PrintHelp ;;
    esac
done

# Check if the module name is provided
if [ -z "$ImageName" ]; then
    echo "No module specified."
    exit 1
fi

# Define the path for the module, default path is the Docker folder in the engineering repo
dockerDir=$(realpath ../..)

# The smartbroker module is in a the datascience folder under Engineering
if [ "$ImageName" == "smartbroker" ]; then
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

# Get the version from the VERSION file
ImageVersionFromFile=$(cat ../../VERSION)

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
                export AZURE_SUBSCRIPTION_ID=$DEVELOPMENT_SUBSCRIPTION_ID
                ResourceGroup=$DEVELOPMENT_RESOURCE_GROUP # This needs to get updated per choice of subscription
                ImageVersion=0.0.0
                break
                ;;
            2)
                echo -e "\n==== Setting env variables for $opt ===="
                export AZURE_SUBSCRIPTION_ID=$RELEASE_CANDIDATE_SUBSCRIPTION_ID
                ResourceGroup=$RELEASE_CANDIDATE_RESOURCE_GROUP # This needs to get updated per choice of subscription
                ImageVersion=$ImageVersionFromFile
                break
                ;;
            3)
                echo -e "\n==== Setting env variables for $opt ===="
                export AZURE_SUBSCRIPTION_ID=$PRODUCTION_GA_SUBSCRIPTION_ID
                ResourceGroup=$PRODUCTION_GA_RESOURCE_GROUP # This needs to get updated per choice of subscription
                ImageVersion=$ImageVersionFromFile
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
--name $ImageName
echo "Deletion Completed, continuing..."

echo -e "\n==== Azure VHD& Image Creation Begins ====\n"
# Create resource group for storage account
az group create \
--name $ResourceGroup \
--location $Location

# Create the shared image gallery
az sig create \
--resource-group $ResourceGroup \
--gallery-name $ImageGalleryName \
--location $Location

# Create the image definition
az sig image-definition create \
--resource-group $ResourceGroup \
--gallery-name $ImageGalleryName \
--gallery-image-definition $ImageName \
--features SecurityType=ConfidentialVMSupported \
--publisher "Secure-AI-Labs" \
--hyper-v-generation V2 \
--offer $ImageName \
--sku "sail" \
--os-type "Linux"

# Ubuntu Image in shared image gallery
output=$(packer build \
-var location=$Location \
-var resource_group_name=$ResourceGroup \
-var module=$ImageName \
-var docker_dir=$dockerDir \
-var gallery_name=$ImageGalleryName \
-var version=$ImageVersion \
packer-sig-ubuntu.json | tee /dev/tty)

# Get the image name from the packer output
ImageName=$(echo "$output" | grep "ManagedImageName:" | cut -d':' -f2 | tr -d '[:space:]')

# Get the short git commit hash
gitCommitHash=$(git rev-parse --short HEAD)

# Tag the image with the short git commit hash
az image update \
--resource-group $ResourceGroup \
--name $ImageName \
--tags gitCommitHash=$gitCommitHash
