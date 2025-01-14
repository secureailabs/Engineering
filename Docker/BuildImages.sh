#!/bin/bash
set -e

PrintHelp() {
    echo ""
    echo "Usage: $0 -i [Image Name]"
    echo "Usage: $0 -i [Image Name] -p"
    echo "Usage: $0"
    echo -e "\t-i Image Name: apiservices | newwebfrontend | rpcrelated | auditserver | smartbroker"
    echo -e "\t-p Specify flag to push built image to the docker registry"
    exit 1 # Exit script after printing help
}

# function to tag and push the input image to the docker hub
PushImageToRegistry() {
    # check if the DOCKER_REGISTRY_NAME is set
    if [ -z "$DOCKER_REGISTRY_NAME" ]; then
        echo "DOCKER_REGISTRY_NAME is not set"
        exit 1
    fi

    #login to azure account
    echo "login to azure account"
    az login --service-principal --username $AZURE_CLIENT_ID --password $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
    az account set --subscription $AZURE_SUBSCRIPTION_ID

    # check if the azure registry is logged in
    echo "log in to azure registry"
    az acr login --name "$DOCKER_REGISTRY_NAME"

    # Get the version from the ../VERSION file
    version=$(cat ../VERSION)

    # Get the current git commit hash
    gitCommitHash=$(git rev-parse --short HEAD)

    echo "Tag and Pushing image to azure hub"
    tag=v"$version"_"$gitCommitHash"
    echo "Tag: $tag"
    docker tag "$1" "$DOCKER_REGISTRY_NAME".azurecr.io/"$1":"$tag"
    docker push "$DOCKER_REGISTRY_NAME".azurecr.io/"$1":"$tag"
    echo Image url: "$DOCKER_REGISTRY_NAME".azurecr.io/"$1":"$tag"
}

# Check if docker is installed
docker --version
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error docker does not exist"
    exit $retVal
fi

# Set the default values for the input parameters
pushImage=false

# Parse the input parameters
while getopts "i:p" opt
do
    echo "opt: $opt $OPTARG"
    case "$opt" in
    i) imageName="$OPTARG" ;;
    p) pushImage=true ;;
    ?) PrintHelp ;;
    esac
done

# Build the asked image if it specified in the input parameters
if [ -z "$imageName" ]; then
    echo "No image specified. Building all of them..."
else
    echo "Building image $imageName"
    docker build -t "$imageName" -f "${imageName}/Dockerfile" .
    if [ "$pushImage" = true ]; then
        PushImageToRegistry "$imageName"
    fi
    exit 0
fi

# Check if all the required files are present on the machine
declare -a ListOfDockerImages=(
    "apiservices"
    "newwebfrontend"
    "rpcrelated"
    "auditserver"
    "smartbroker"
)

for val in "${ListOfDockerImages[@]}"; do
    echo -e "\nBuilding for $val ..."
    docker build -t "$val" -f "${val}/Dockerfile" .
    if [ "$pushImage" = true ]; then
        PushImageToRegistry "$val"
    fi
done

echo "--------------------------------------------------"
echo "cleaning up"
echo "--------------------------------------------------"
(cd ../ && make clean_datascience)
