#!/bin/bash
set -e

PrintHelp() {
    echo ""
    echo "Usage: $0 -i [Image Name]"
    echo "Usage: $0 -i [Image Name] -p"
    echo "Usage: $0"
    echo -e "\t-i Image Name: apiservices | newwebfrontend | rpcrelated | auditserver"
    exit 1 # Exit script after printing help
}

# function to tag and push the input image to the docker hub
PushImageToRegistry() {
    # check if the CONTAINER_REGISTRY_NAME is set
    if [ -z "$CONTAINER_REGISTRY_NAME" ]; then
        echo "CONTAINER_REGISTRY_NAME is not set"
        exit 1
    fi

    # check if the azure registry is logged in
    echo "log in to azure registry"
    az acr login --name "$CONTAINER_REGISTRY_NAME"

    # Get the version from the ../VERSION file
    version=$(cat ../VERSION)

    # Get the current git commit hash
    gitCommitHash=$(git rev-parse --short HEAD)

    echo "Tag and Pushing image to azure hub"
    tag=v"$version"_"$gitCommitHash"
    docker tag "$1" "$CONTAINER_REGISTRY_NAME".azurecr.io/"$1":"$tag"
    docker push "$CONTAINER_REGISTRY_NAME".azurecr.io/"$1":"$tag"
}

# Check if docker is installed
docker --version
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error docker does not exist"
    exit $retVal
fi

# Parse the input parameters
while getopts "i:p" opt; do
    echo "opt: $opt $OPTARG"
    case "$opt" in
    p) pushImage=true ;;
    i) imageName="$OPTARG" ;;
    ?) PrintHelp ;;
    esac
done

echo "--------------------------------------------------"
echo "making apiservice package"
echo "--------------------------------------------------"
(cd ../ && make package_apiservices)

echo "--------------------------------------------------"
echo "--------------------------------------------------"
# Prune unused docker networks
docker network prune -f
echo "--------------------------------------------------"
echo "--------------------------------------------------"

# Create sailNetwork if it does not exist
networkName="sailNetwork"
foundNetworkName=$(docker network ls --filter name=$networkName --format {{.Name}})
echo "$foundNetworkName"
if [ "$foundNetworkName" == "$networkName" ]; then
    echo "Network already exists"
else
    echo "Creating network"
    docker network create --subnet=172.31.252.0/24 $networkName
fi
echo "--------------------------------------------------"
docker network ls
echo "--------------------------------------------------"
echo "--------------------------------------------------"

# Build the asked image if it specified in the input parameters
if [ -z "$imageName" ]; then
    echo "No image specified. Building all of them..."
else
    echo "Building image $imageName"
    docker build -t "$imageName" -f "$imageName"/Dockerfile .
    if $pushImage; then
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
)

for val in "${ListOfDockerImages[@]}"; do
    echo -e "\nBuilding for ${val} ..."
    docker build . -t "${val}"
    if $pushImage; then
        PushImageToRegistry "$val"
    fi
done

echo "--------------------------------------------------"
echo "cleaning up"
echo "--------------------------------------------------"
(cd ../ && make clean_datascience)
