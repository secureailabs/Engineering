#!/bin/bash
imageName=rpcrelated

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
-dit \
-p 5556:5556 \
-p 9090:9091 \
--cap-add=SYS_ADMIN \
--cap-add=DAC_READ_SEARCH \
--privileged \
-v $(pwd)/"$imageName"_dir:/app \
-v $(pwd)/certs:/etc/nginx/certs \
$imageName
