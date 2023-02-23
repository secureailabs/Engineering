#!/bin/bash
export tempDeployDir=$(mktemp -d --tmpdir=.)

# This is part 1 of a series of scripts to run to quickly delete resources from azure.

PrintHelp()
{
    echo ""
    echo "Usage: $0 -o [Owner: [Prawal, Stanley]]"
    echo -e "\t-o Triggered By: deployment owner name. No spaces."
    exit 1 # Exit script after printing help
}

# Check if docker is installed
docker --version
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error docker does not exist"
    exit $retVal
fi

# Parse the input parameters
while getopts "o:" opt
do
    echo "opt: $opt $OPTARG"
    case "$opt" in
        o ) owner="$OPTARG" ;;
        ? ) PrintHelp ;;
    esac
done

# Print Help in case parameters are not correct
if [ -z "$owner" ]
then
    PrintHelp
fi
echo "Owner: $owner"

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
if [ -z "${AZURE_OBJECT_ID}" ]; then
    echo "environment variable AZURE_OBJECT_ID is undefined"
    exit 1
fi


# Set the subscription for SAIL GLOBAL HUB
rgpipName="rg-sail-wus-hubpipdev-001"
rgfwName="rg-sail-wus-hub-001"
azName="afw-sail-wus"

echo -e "==== Login to Azure and Set Subscription ====\n"
az login --service-principal --username $AZURE_CLIENT_ID --password $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
az account set --subscription $AZURE_SUBSCRIPTION_ID
# az account set --subscription '6e7f356c-6059-4799-b83a-c4744e4a7c2e'
echo -e "\n==== Verify Subscription Set Properly ====\n"
az account show

# List out resources for visualization based on query parameters
echo -e "\nPlease Specify # for resource search parameters: "
options=("Platform Services" "SCN" "Platform Services and SCN" "Quit")
select opt in "${options[@]}"
do
    case $REPLY in
        1)  
            output=$(az group list --tag deployed_method="DeployPlatform" --query "[?contains(name,'$owner')].{name:name}" --output tsv)
            break
            ;;
        2)
            output=$(az group list --tag module="scn" --query "[?contains(name,'$owner')].{name:name}" --output tsv)
            break
            ;;
        3)
            output=$(az group list --query "[?contains(name,'$owner')].{name:name}" --output tsv)
            break
            ;;
        4)
            exit 0
            ;;
    esac
done

echo -e "\nThe following resources were found:\n$output\n"
# Delete the resources based on selected options
echo -e "Please Specify # : "
options=("Delete resources of specified guid" "Delete all resources associated with owner" "Quit")
select opt in "${options[@]}"
do
    case $REPLY in
        1)  
            echo "Deleting resources of specified guid!"
            while true; do
                read -p "Enter guid of platform you wish to delete: " GUID
                if [ -z $GUID ]; then
                    echo "GUID entered was empty; exiting..."
                    exit 0
                fi
                echo -e "\nList of Resources staged for deletion\n"
                GUID="${GUID//[[:space:]]/}"
                echo -e "The following resources were found based on inputed GUID:|$GUID|\n"
                az group list --query "[?contains(name,'$GUID')].{name:name}" --output tsv
                read -p "Do you wish to continue?  " yn
                case $yn in
                    [Yy]* ) 
                        echo -e "PROCEEDING...\n"
                        for rgname in `az group list --query "[?contains(name,'$GUID')].{name:name}" --output tsv`; do
                            echo Deleting ${rgname}
                            az group delete -n ${rgname} --yes --no-wait
                        done
                        break
                        ;;
                    [Nn]* ) continue;;
                    * ) echo "Please answer yes or no.";;
                esac
            done
            break
            ;;
        2)
            echo -e "\nDeleting all resources associated with specified owner!\n"
            az group list --query "[?contains(name,'$owner')].{name:name}" --output tsv
            read -p "Do you wish to continue?  " yn
                case $yn in
                    [Yy]* ) 
                        echo "PROCEEDING..."
                        for rgname in `az group list --query "[?contains(name,'$owner')].{name:name}" --output tsv`; do
                            echo Deleting ${rgname}
                            az group delete -n ${rgname} --yes --no-wait
                        done
                        break
                        ;;
                    [Nn]* ) continue;;
                    * ) echo "Please answer yes or no.";;
                esac
            break
            ;;
        3)
            exit 0
            ;;
    esac
done

echo "=============================================================="
echo -e "\nCOMPLETED deleting of ResourceGroups based on Query."
echo -e "Please wait a few moments and verify deletion of resources in azure\n"
echo "=============================================================="