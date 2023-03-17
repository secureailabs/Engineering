#!/bin/bash
set -e

PrintHelp() {
    echo ""
    echo "Usage: $0 -s [Service Name] -d -c"
    echo -e "\t-s Service Name: newwebfrontend | apiservices | rpcrelated | auditserver"
    echo -e "\t-d Run docker container detached"
    echo -e "\t-c Clean the database"
    echo -e "\t-n Name to give the running docker image"
    echo -e "\t-t Optional tag (will default to 'latest')"
    exit 1 # Exit script after printing help
}

# Parese the input parameters
detach=false
cleanDatabase=false
dockerName=""
while getopts "s:n:t:d:l opt:c opt:" opt; do
    echo "opt: $opt $OPTARG"
    case "$opt" in
    s) imageName="$OPTARG" ;;
    d) detach=true ;;
    c) cleanDatabase=true ;;
    l) localDataset="$OPTARG" ;;
    n) dockerName="$OPTARG" ;;
    t) imageTag="$OPTARG" ;;
    ?) PrintHelp ;;
    esac
done

# Print Help in case parameters are not correct
if [ -z "$imageName" ] || [ -z "$detach" ]; then
    PrintHelp
fi

if [ -z "$dockerName" ]; then
    dockerName=$imageName
fi
echo "Running $imageName"
echo "Tag: $imageTag"
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
if [ "$imageNameFound" == "$imageName" ]; then
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

# Create a folder to hold all the Binaries
rm -rf $rootDir/Binary/"$imageName"_dir
mkdir -p $rootDir/Binary/"$imageName"_dir


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
docker network ls

# Prepare the flags for the docker run command
runtimeFlags="$detachFlags --name $dockerName --network $networkName -v $rootDir/DevopsConsole/certs:/etc/nginx/certs"
# TODO: issue because sailNetwork is shared.
if [ "apiservices" == "$imageName" ]; then
    # Create database volume if it does not exist
    foundVolumeName=$(docker volume ls --filter name=$sailDatabaseVolumeName --format {{.Name}})
    echo "$foundVolumeName"
    if [ "$foundVolumeName" == "$sailDatabaseVolumeName" ]; then
        echo "Database Volume already exists"
    else
        echo "Creating database volume"
        docker volume create $sailDatabaseVolumeName
    fi
    make -C $rootDir package_apiservices -s
    cp apiservices/InitializationVector.json $rootDir/Binary/apiservices_dir
    cat $rootDir/Binary/apiservices_dir/InitializationVector.json
    cp $rootDir/Binary/apiservices.tar.gz $rootDir/Binary/apiservices_dir/package.tar.gz
    runtimeFlags="$runtimeFlags -p 8000:8001 -p 9080:9080 -v $sailDatabaseVolumeName:/srv/mongodb/db0 -v $rootDir/Binary/apiservices_dir:/app $imageName"
elif [ "newwebfrontend" == "$imageName" ]; then
    make -C $rootDir package_newwebfrontend -s
    cp newwebfrontend/InitializationVector.json $rootDir/Binary/newwebfrontend_dir
    cp $rootDir/Binary/newwebfrontend.tar.gz $rootDir/Binary/newwebfrontend_dir/package.tar.gz
    runtimeFlags="$runtimeFlags -p 443:443 -v $rootDir/Binary/newwebfrontend_dir:/app $imageName:$imageTag"
elif [ "newwebfrontend2" == "$imageName" ]; then
    make -C $rootDir package_newwebfrontend -s
    cp newwebfrontend/InitializationVector.json $rootDir/Binary/newwebfrontend_dir
    cp $rootDir/Binary/newwebfrontend.tar.gz $rootDir/Binary/newwebfrontend_dir/package.tar.gz
    runtimeFlags="$runtimeFlags -p 443:443 -v $rootDir/Binary/newwebfrontend_dir:/app $imageName:$imageTag"
elif [ "rpcrelated" == "$imageName" ]; then
    cp rpcrelated/InitializationVector.json $rootDir/Binary/rpcrelated_dir
    if [ ! -f $rootDir/Binary/rpcrelated_dir/package.tar.gz ]; then
        echo "RPC Package not found, building"
        pushd $rootDir/RPCLib/
        ./package.sh
        popd
    fi
    if [ $localDataset ]; then
        runtimeFlags="$runtimeFlags -v $localDataset:/local_dataset"
    fi
    runtimeFlags="$runtimeFlags --cap-add=SYS_ADMIN --cap-add=DAC_READ_SEARCH --privileged -v $rootDir/Binary/rpcrelated_dir:/app $imageName"
elif [ "auditserver" == "$imageName" ]; then
    make -C $rootDir package_audit_service -s -j
    cp $rootDir/Binary/audit_server.tar.gz $rootDir/Binary/audit_server_dir/package.tar.gz
    runtimeFlags="$runtimeFlags -p 3100:3100 -p 9093:9093 -p 9096:9096 $imageName"
else
    echo "!!! Kindly provide correct service name !!!"
    PrintHelp
fi

# Run the docker container
docker run $runtimeFlags
