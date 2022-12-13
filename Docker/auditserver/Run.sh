#!/bin/bash
imageName=auditserver

# Check if docker is installed
docker --version
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error docker does not exist"
    exit $retVal
fi

# Check if the image exists
imageNameFound=$(docker image ls --filter reference=$imageName --format {{.Repository}})
echo "$imageNameFound"
if [ "$imageNameFound" == "$imageName" ]
then
    echo "Docker image exists"
else
    echo "!!! Docker image not found !!!"
    exit 1
fi

# Create a folder to hold all the Binaries
mkdir -p "$imageName"_dir

# Copy the binaries to the folder
cp vm_initializer.py "$imageName"_dir/

# Run the docker container
docker run \
-it \
-p 3100:3100 \
-p 9093:9093 \
-p 9096:9096 \
-v $(pwd)/"$imageName"_dir:/app \
--name auditserver \
$imageName
