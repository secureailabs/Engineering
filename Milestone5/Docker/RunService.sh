#!/bin/bash
set -e

PrintHelp()
{
    echo ""
    echo "Usage: $0 -s [Service Name] -d"
    echo -e "\t-s Service Name: backend | orchestrator | remotedataconnector | webfrontend | securecomputationnode"
    echo -e "\t-d Run docker container detached"
    exit 1 # Exit script after printing help
}

# Parese the input parameters
detach=false
while getopts "s:d opt:" opt
do
    case "$opt" in
        s ) imageName="$OPTARG" ;;
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
imageNameFound=$(docker image ls --filter reference="$imageName" --format {{.Repository}})
echo "$imageNameFound"
if [ "$imageNameFound" == "$imageName" ]
then
    echo "Docker image exists"
else
    echo "!!! Kindly create the docker image using BuildImages.sh !!!"
    exit 1
fi

# Set the root directory of the whole platform
rootDir=$(pwd)/..

# Prepare the flags for the docker run command
runtimeFlags="$detachFlags --name $imageName --network sailNetwork"
if [ "orchestrator" == "$imageName" ]
then
    cp orchestrator/InitializationVector.json $rootDir/VirtualMachine/Orchestrator
    runtimeFlags="$runtimeFlags -p 8080:8080 -v $rootDir/VirtualMachine/Orchestrator:/app $imageName"
elif [ "backend" == "$imageName" ]
then
    cp backend/InitializationVector.json $rootDir/Binary
    runtimeFlags="$runtimeFlags --hostname backend -p 6200:6200 -v $rootDir/Binary:/app $imageName"
elif [ "webfrontend" == "$imageName" ]
then
    cp webfrontend/InitializationVector.json $rootDir/WebFrontend
    runtimeFlags="$runtimeFlags -p 3000:3000 -v $rootDir/WebFrontend:/app $imageName"
elif [ "securecomputationnode" == "$imageName" ]
then
    cp securecomputationnode/InitializationVector.json $rootDir/Binary
    runtimeFlags="$runtimeFlags -p 3500:3500 -p 6800:6800 -v $rootDir/Binary:/app $imageName"
elif [ "remotedataconnector" == "$imageName" ]
then
    echo "!!! NOT IMPLEMENTED !!!"
    exit 1
    # runtimeFlags="$runtimeFlags -v $rootDir/Binary:/Development $imageName"
else
    echo "!!! Kindly provide correct service name !!!"
    PrintHelp
fi

# Run the docker container
docker run $runtimeFlags
