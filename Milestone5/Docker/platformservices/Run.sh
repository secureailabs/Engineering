#!/bin/bash
imageName=platformservices

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

# Move the InitializerVector to the Binary folder
mv InitializationVector.json Binary/$imageName

# Run the docker container
docker run \
-dit \
-p 6200:6200 \
-v $(pwd)/Binary/$imageName:/app \
$imageName
