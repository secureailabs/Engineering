#!/bin/bash
set -e

networkName="sailNetwork"
imageName="frontend"

foundNetworkName=$(docker network ls --filter name=$networkName --format {{.Name}})
echo $foundNetworkName

if [ "$foundNetworkName" == "$networkName" ]
then
    echo "Network already exists"
else
    echo "Creating network"
    docker network create $networkName
fi

# Build the frontend image
docker build . -t $imageName
