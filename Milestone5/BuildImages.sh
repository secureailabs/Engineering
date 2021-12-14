#!/bin/bash
set -e

networkName="sailNetwork"
backendImageName="backend"
orchestratorImageName="orchestrator"
remoteDataConnectorImageName="remotedataconnector"

foundNetworkName=$(docker network ls --filter name=$networkName --format {{.Name}})
echo $foundNetworkName

if [ "$foundNetworkName" == "$networkName" ]
then
    echo "Network already exists"
else
    echo "Creating network"
    docker network create $networkName
fi

# Buid the backend image
docker build -f Docker/Dockerfile.Backend . -t $backendImageName

# Build the orchestrator image
docker build -f Docker/Dockerfile.Orchestrator . -t $orchestratorImageName

# Build the Remote DataConnector image
docker build -f Docker/Dockerfile.RemoteDataConnector . -t $remoteDataConnectorImageName
