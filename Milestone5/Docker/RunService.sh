#!/bin/bash
set -e

PrintHelp()
{
    echo ""
    echo "Usage: $0 -s [Service Name] -d -c"
    echo -e "\t-s Service Name: platformservices | dataservices | orchestrator | remotedataconnector | webfrontend | securecomputationnode | devopsconsole"
    echo -e "\t-d Run docker container detached"
    echo -e "\t-c Clean the database"
    exit 1 # Exit script after printing help
}

# Parese the input parameters
detach=false
cleanDatabase=false
while getopts "s:d opt:c opt:" opt
do
    case "$opt" in
        s ) imageName="$OPTARG" ;;
        d ) detach=true ;;
        c ) cleanDatabase=true ;;
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
echo "Clean Database: $cleanDatabase"

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

# Clean up existing non-running containers
echo "Cleaning existing non-running containers"
docker container rm -f $imageName

# Set the root directory of the whole platform
rootDir=$(pwd)/..

# Sail Database volume name
sailDatabaseVolumeName="sailDatabase"

# Clean the database if the cleanDatabase flag exists
if $cleanDatabase; then
    echo "Cleaning database"
    docker volume rm -f $sailDatabaseVolumeName
fi

# Prepare the flags for the docker run command
runtimeFlags="$detachFlags --name $imageName --network sailNetwork"

if [ "orchestrator" == "$imageName" ]
then
    cp orchestrator/InitializationVector.json $rootDir/EndPointTools/Orchestrator/sail
    runtimeFlags="$runtimeFlags -p 8080:8080 -v $rootDir/EndPointTools/Orchestrator/sail:/app $imageName"
elif [ "devopsconsole" == "$imageName" ]
then
    cp devopsconsole/InitializationVector.json $rootDir/DevopsConsole
    runtimeFlags="$runtimeFlags -v $rootDir/DevopsConsole:/app -v $rootDir/DevopsConsole/nginx:/etc/nginx/conf.d -v $rootDir/DevopsConsole/certs:/etc/nginx/certs -p 5050:443 $imageName"
elif [ "dataservices" == "$imageName" ]
then
    # Create database volume if it does not exist
    foundVolumeName=$(docker volume ls --filter name=$sailDatabaseVolumeName --format {{.Name}})
    echo "$foundVolumeName"
    if [ "$foundVolumeName" == "$sailDatabaseVolumeName" ]
    then
        echo "Database Volume already exists"
    else
        echo "Creating database volume"
        docker volume create $sailDatabaseVolumeName
    fi
    # Copy InitializationVector.json to the dataservices
    cp dataservices/InitializationVector.json $rootDir/Binary/dataservices
    runtimeFlags="$runtimeFlags --hostname dataservices -p 6500:6500 -v $sailDatabaseVolumeName:/srv/mongodb/db0 -v $rootDir/Binary/dataservices:/app $imageName"
elif [ "platformservices" == "$imageName" ]
then
    # Copy InitializationVector.json to the platformservices
    cp platformservices/InitializationVector.json $rootDir/Binary/platformservices
    runtimeFlags="$runtimeFlags --hostname platformservices -p 6200:6200 -v $rootDir/Binary/platformservices:/app $imageName"
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
