#!/bin/bash
imageName=apiservices

# Check if docker is installed
docker --version
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error docker does not exist"
    exit $retVal
fi

# Create a folder to hold all the Binaries
mkdir -p "$imageName"_dir

# Run the docker container
docker run \
-dit \
-p 8000:8001 \
-p 9090:9091 \
-v $(pwd)/"$imageName"_dir:/app \
-v $(pwd)/certs:/etc/nginx/certs \
$imageName
