#!/bin/bash
set -e

PrintHelp() {
    echo ""
    echo "Usage: $0 -i [Image Name]"
    echo "Usage: $0"
    echo -e "\t-i Image Name: apiservices | devopsconsole | webfrontend | newwebfrontend | orchestrator | remotedataconnector | securecomputationnode"
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
while getopts "i:" opt; do
    echo "opt: $opt $OPTARG"
    case "$opt" in
    i) imageName="$OPTARG" ;;
    ?) PrintHelp ;;
    esac
done

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
    pushd "$imageName"
    docker build . -t "$imageName"
    # TODO: Prawal
    # docker build . -t "$imageName:$(git rev-parse --short HEAD)"
    popd
    exit 0
fi

# Check if all the required files are present on the machine
declare -a ListOfDockerImages=(
    "apiservices"
    "orchestrator"
    "remotedataconnector"
    "webfrontend"
    "newwebfrontend"
    "securecomputationnode"
    "devopsconsole"
    "rpcrelated"
)

for val in "${ListOfDockerImages[@]}"; do
    echo -e "\nBuilding for ${val} ..."
    pushd "${val}"
    docker build . -t "${val}"
    popd
done
