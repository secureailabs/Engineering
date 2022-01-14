#!/bin/bash
set -e

PrintHelp()
{
    echo ""
    echo "Usage: $0 -d"
    echo -e "\t-d Run docker container detached"
    exit 1 # Exit script after printing help
}

# Parese the input parameters
detach=false
imageName="frontend"
while getopts "d opt:" opt
do
    case "$opt" in
        d ) detach=true ;;
        ? ) PrintHelp ;;
    esac
done

# Print Help in case parameters are not correct
if [ -z "$imageName" ] || [ -z "$detach" ]
then
    PrintHelp
fi
echo "Running $imageName"
echo "Detach: $detach"

# If the detach flag exists, run the container in the background
# Default behaviour is to run the container in the foreground
detachFlags=-it
if $detach; then
    detachFlags=-dit
fi

# Check if the image exists
imageNameFound=$(docker image ls --filter reference=$imageName --format {{.Repository}})
echo $imageNameFound
if [ "$imageNameFound" == "$imageName" ]
then
    echo "Docker image exists"
else
    echo "!!! Kindly create the docker image using BuildImages.sh !!!"
    exit 1
fi

# Run the docker container
docker run \
    $detachFlags \
    --network sailNetwork \
    -p 3000:3000 \
    -v $(pwd):/app \
    $imageName
