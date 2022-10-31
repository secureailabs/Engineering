#!/bin/bash

# Remember to decrypt .env.dev.encrypted with 'npm run env:decrypt'
source .env.dev
Location="westus"
ResourceGroup=$AZURE_RESOURCE_GROUP
StorageAccountName=$AZURE_STORAGE_ACCOUNT
GIT=$(git rev-parse --short HEAD)
PrintHelp()
{
    echo ""
    echo "Usage: $0 -m [Image Name] [-a]"
    echo "Usage: $0"
    echo -e "\t-m Module Name:  apiservices | orchestrator | remotedataconnector | webfrontend | newwebfrontend | securecomputationnode | rpcrelated"
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
                StorageAccountName=$DEVELOPMENT_STORAGE_ACCOUNT_NAME # This needs to get updated per choice of subscription
                break
                ;;
            2)
                echo -e "\n==== Setting env variables for $opt ===="
                export AZURE_SUBSCRIPTION_ID=$RELEASE_CANDIDATE_SUBSCRIPTION_ID
                ResourceGroup=$RELEASE_CANDIDATE_RESOURCE_GROUP # This needs to get updated per choice of subscription
                StorageAccountName=$RELEASE_CANDIDATE_STORAGE_ACCOUNT_NAME # This needs to get updated per choice of subscription
                break
                ;;
            3)
                echo -e "\n==== Setting env variables for $opt ===="
                export AZURE_SUBSCRIPTION_ID=$PRODUCTION_GA_SUBSCRIPTION_ID
                ResourceGroup=$PRODUCTION_GA_RESOURCE_GROUP # This needs to get updated per choice of subscription
                StorageAccountName=$PRODUCTION_GA_STORAGE_ACCOUNT_NAME # This needs to get updated per choice of subscription
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

# Create storage account
az storage account create \
--resource-group $ResourceGroup \
--name $StorageAccountName \
--location $Location \
--sku Standard_LRS \
--kind StorageV2 \
--access-tier Hot

# Ubuntu vhd Image
output=$(packer build \
-var location=$Location \
-var storage_resource_group=$ResourceGroup \
-var storage_account=$StorageAccountName \
-var module=$imageName \
packer-vhd-ubuntu.json | tee /dev/tty)

# Specify vhdImageUrl to use
temp=$(echo "$output" | grep -Po "OSDiskUri: (https:*.*sailimages.*.vhd)")
vhdImageUrl=$(echo "$temp" | grep -Po "https:*.*vhd")

# Create managed image from vhd
az image create \
--resource-group $ResourceGroup \
--name $imageName \
--source $vhdImageUrl \
--location $Location \
--os-type "Linux" \
--storage-sku "Standard_LRS" \
--tags git=$GIT

# # Optionally to create a VM with the image
# az vm create \
# --resource-group $ResourceGroup \
# --name "$imageName"Vm \
# --image $imageName \
# --admin-username saildeveloper \
# --admin-password "Password@123"

# # Optionally upload the packages to the Virtual VirtualMachine
# ./UploadPackageAndInitializationVector --IpAddress=<VmIp> --Package=PlatformServices.tar.gz --InitializationVector=InitializationVector.json
