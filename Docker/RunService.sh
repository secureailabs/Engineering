#!/bin/bash
set -e

PrintHelp() {
    echo ""
    echo "Usage: $0 -s [Service Name] -d -c"
    echo -e "\t-s Service Name: devopsconsole | dataservices | platformservices | webfrontend | orchestrator | remotedataconnector | securecomputationnode"
    echo -e "\t-d Run docker container detached"
    echo -e "\t-c Clean the database"
    exit 1 # Exit script after printing help
}

# Parese the input parameters
detach=false
cleanDatabase=false
while getopts "s:d opt:c opt:" opt; do
    case "$opt" in
    s) imageName="$OPTARG" ;;
    d) detach=true ;;
    c) cleanDatabase=true ;;
    ?) PrintHelp ;;
    esac
done

# Print Help in case parameters are not correct
if [ -z "$imageName" ] || [ -z "$detach" ]; then
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

# Build the bootstrap tool to create the database
make -C $rootDir baseVmInit -s -j

# Create a folder to hold all the Binaries
rm -rf $rootDir/Binary/"$imageName"_dir
mkdir -p $rootDir/Binary/"$imageName"_dir

# Copy the binaries to the folder
cp $rootDir/Binary/BaseVmImageInit $rootDir/Binary/"$imageName"_dir/

# Prepare the flags for the docker run command
runtimeFlags="$detachFlags --name $imageName --network sailNetwork -v $rootDir/DevopsConsole/nginx:/etc/nginx/conf.d -v $rootDir/DevopsConsole/certs:/etc/nginx/certs"
# runtimeFlags="$detachFlags --name $imageName"
# TODO: issue because sailNetwork is shared.
if [ "orchestrator" == "$imageName" ]; then
    cp orchestrator/InitializationVector.json $rootDir/EndPointTools/Orchestrator/sail
    runtimeFlags="$runtimeFlags -p 8080:8080 -v $rootDir/EndPointTools/Orchestrator/sail:/app -v $rootDir/EndPointTools/SafeObjectTools/SafeObjects:/SafeObjects $imageName"
elif [ "devopsconsole" == "$imageName" ]; then
    cp devopsconsole/InitializationVector.json $rootDir/DevopsConsole
    runtimeFlags="$runtimeFlags -v $rootDir/DevopsConsole:/app -p 5050:443 $imageName"
elif [ "dataservices" == "$imageName" ]; then
    # Create database volume if it does not exist
    foundVolumeName=$(docker volume ls --filter name=$sailDatabaseVolumeName --format {{.Name}})
    echo "$foundVolumeName"
    if [ "$foundVolumeName" == "$sailDatabaseVolumeName" ]; then
        echo "Database Volume already exists"
    else
        echo "Creating database volume"
        docker volume create $sailDatabaseVolumeName
    fi
    # Copy InitializationVector.json to the dataservices
    make -C $rootDir package_dataservices -s -j
    cp dataservices/InitializationVector.json $rootDir/Binary/dataservices_dir
    cp $rootDir/Binary/DataServices.tar.gz $rootDir/Binary/dataservices_dir/package.tar.gz
    runtimeFlags="$runtimeFlags -p 6500:6500 --ip 172.31.252.2 -v $sailDatabaseVolumeName:/srv/mongodb/db0 -v $rootDir/Binary/dataservices_dir:/app $imageName"
elif [ "platformservices" == "$imageName" ]; then
    # Copy InitializationVector.json to the platformservices
    make -C $rootDir package_securecomputationnode -s -j
    make -C $rootDir package_platformservices -s -j
    cp platformservices/InitializationVector.json $rootDir/Binary/platformservices_dir
    cp $rootDir/Binary/PlatformServices.tar.gz $rootDir/Binary/platformservices_dir/package.tar.gz
    cp $rootDir/Binary/SecureComputationNode.tar.gz $rootDir/Binary/platformservices_dir/
    runtimeFlags="$runtimeFlags -p 6200:6201 -v $rootDir/Binary/platformservices_dir:/app $imageName"
elif [ "webfrontend" == "$imageName" ]; then
    make -C $rootDir package_webfrontend -s -j
    cp webfrontend/InitializationVector.json $rootDir/Binary/webfrontend_dir
    cp $rootDir/Binary/webfrontend.tar.gz $rootDir/Binary/webfrontend_dir/package.tar.gz
    runtimeFlags="$runtimeFlags -p 3000:3000 -v $rootDir/Binary/webfrontend_dir:/app $imageName"
elif [ "securecomputationnode" == "$imageName" ]; then
    make -C $rootDir package_securecomputationnode -s -j
    cp $rootDir/Binary/SecureComputationNode.tar.gz $rootDir/Binary/securecomputationnode_dir/package.tar.gz
    cp securecomputationnode/InitializationVector.json $rootDir/Binary/securecomputationnode_dir
    runtimeFlags="$runtimeFlags -p 3500:3500 -p 6800:6801 -v $rootDir/Binary/securecomputationnode_dir:/app $imageName"
elif [ "remotedataconnector" == "$imageName" ]; then
    echo "!!! NOT IMPLEMENTED !!!"
    exit 1
    # runtimeFlags="$runtimeFlags -v $rootDir/Binary:/Development $imageName"
else
    echo "!!! Kindly provide correct service name !!!"
    PrintHelp
fi

# Run the docker container
docker run $runtimeFlags
