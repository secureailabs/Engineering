#!/bin/bash

source azure_constants.sh
# Get the version from the VERSION file
ImageVersionFromFile=$(cat ../../VERSION)
ImageVersion=0.0.0 # change the version manually or use ImageVersionFromFile

PrintHelp()
{
    echo ""
    echo "Usage: $0 -m [Image Name] [-a]"
    echo "Usage: $0"
    echo -e "\t-m Module Name:  apiservices | orchestrator | remotedataconnector | webfrontend | newwebfrontend | securecomputationnode | rpcrelated | smartbroker | auditserver"
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

if [ -z "$ci_flag" ]; then
    # Bash Menu
    # TODO Technially all subscriptions for this script can share 1 SP: Discussion We should create singular SP for PACKER
    echo -e "\nPlease Specify # for targeted subscription to upload image: "
    options=("Development" "Release Candidate" "ProductionGA" "Test" "Quit")
    select opt in "${options[@]}"
    do
        case $REPLY in
            1)
                echo -e "\n==== Setting env variables for $opt ===="
                export AZURE_SUBSCRIPTION_ID=$DEVELOPMENT_SUBSCRIPTION_ID
                RESOURCE_GROUP=$DEVELOPMENT_RESOURCE_GROUP # This needs to get updated per choice of subscription
                ImageVersion=0.0.0
                break
                ;;
            2)
                echo -e "\n==== Setting env variables for $opt ===="
                export AZURE_SUBSCRIPTION_ID=$RELEASE_CANDIDATE_SUBSCRIPTION_ID
                RESOURCE_GROUP=$RELEASE_CANDIDATE_RESOURCE_GROUP # This needs to get updated per choice of subscription
                ImageVersion=$ImageVersionFromFile
                break
                ;;
            3)
                echo -e "\n==== Setting env variables for $opt ===="
                export AZURE_SUBSCRIPTION_ID=$PRODUCTION_GA_SUBSCRIPTION_ID
                RESOURCE_GROUP=$PRODUCTION_GA_RESOURCE_GROUP # This needs to get updated per choice of subscription
                ImageVersion=$ImageVersionFromFile
                break
                ;;
            4)
                echo -e "\n==== Setting env variables for $opt ===="
                export AZURE_SUBSCRIPTION_ID=$DEVELOPMENT_SUBSCRIPTION_ID
                ResourceGroup="sail_test" # This needs to get updated per choice of subscription
                StorageAccountName="sailvmimages9998" # This needs to get updated per choice of subscription
                break
                ;;
            5)
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
--resource-group $RESOURCE_GROUP)
echo "$output"

# Delete old custom SAIL managed images
echo -e "\n==== Azure Image Delete As Required ====\n"
az image delete \
--resource-group $RESOURCE_GROUP \
--name $ImageName
echo "Deletion Completed, continuing..."

az sig image-version delete \
--gallery-image-version $ImageVersion \
--gallery-image-definition $ImageName \
--gallery-name $ImageGalleryName \
--resource-group $ResourceGroup
echo "Image Version Deletion Completed, continuing..."

echo -e "\n==== Azure Managed Image Creation Begins ====\n"
# Create resource group for storage account
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
-var location=$LOCATION \
-var resource_group_name=$RESOURCE_GROUP \
-var module=$ImageName \
-var docker_dir=$dockerDir \
-var gallery_name=$IMAGE_GALLERY_NAME \
-var version=$ImageVersion \
-var gitCommitHash=$gitCommitHash \
packer-sig-ubuntu.json

# Tag the image with the short git commit hash
az image update \
--resource-group $RESOURCE_GROUP \
--name $ImageName \
--tags gitCommitHash=$gitCommitHash
