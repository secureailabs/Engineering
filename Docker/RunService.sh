#!/bin/bash
set -e

PrintHelp() {
    echo ""
    echo "Usage: $0 -s [Service Name] -d -c"
    echo -e "\t-s Service Name: devopsconsole | webfrontend | newwebfrontend | orchestrator | remotedataconnector | securecomputationnode | rpcrelated | auditserver"
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
make -C $rootDir vmInitializer -s

# Create a folder to hold all the Binaries
rm -rf $rootDir/Binary/"$imageName"_dir
mkdir -p $rootDir/Binary/"$imageName"_dir

# Copy the binaries to the folder
cp $rootDir/Binary/vm_initializer.py $rootDir/Binary/"$imageName"_dir/

# Prepare the flags for the docker run command
runtimeFlags="$detachFlags --name $imageName --network sailNetwork -v $rootDir/DevopsConsole/certs:/etc/nginx/certs"
# TODO: issue because sailNetwork is shared.
if [ "orchestrator" == "$imageName" ]; then
    make -C $rootDir orchestrator -s
    cp orchestrator/InitializationVector.json $rootDir/EndPointTools/Orchestrator/sail
    runtimeFlags="$runtimeFlags -p 8080:8080 -v $rootDir/EndPointTools/Orchestrator/sail:/app -v $rootDir/EndPointTools/SafeObjectTools/SafeObjects:/SafeObjects $imageName"
elif [ "devopsconsole" == "$imageName" ]; then
    cp devopsconsole/InitializationVector.json $rootDir/DevopsConsole
    runtimeFlags="$runtimeFlags -v $rootDir/DevopsConsole:/app -p 5050:443 $imageName"
elif [ "apiservices" == "$imageName" ]; then
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
    # Check for Azure environment variables
    if [ -z "${AZURE_SUBSCRIPTION_ID}" ]; then
        echo "environment variable AZURE_SUBSCRIPTION_ID is undefined. Using development as default."
        AZURE_SUBSCRIPTION_ID="b7a46052-b7b1-433e-9147-56efbfe28ac5"
        # exit 1
    fi
    if [ ${AZURE_SUBSCRIPTION_ID} == "3d2b9951-a0c8-4dc3-8114-2776b047b15c" ]; then
        cp apiservices/InitializationVectorScratchPad.json.bak $rootDir/Binary/apiservices_dir/InitializationVector.json
    elif  [ ${AZURE_SUBSCRIPTION_ID} == "b7a46052-b7b1-433e-9147-56efbfe28ac5" ]; then
        cp apiservices/InitializationVectorDevelopment.json.bak $rootDir/Binary/apiservices_dir/InitializationVector.json
    elif  [${AZURE_SUBSCRIPTION_ID} == "40cdb551-8a8d-401f-b884-db1599022002" ]; then
        cp apiservices/InitializationVectorReleaseCandidate.json.bak $rootDir/Binary/apiservices_dir/InitializationVector.json
    elif  [ ${AZURE_SUBSCRIPTION_ID} == "ba383264-b9d6-4dba-b71f-58b3755382d8" ]; then
        cp apiservices/InitializationVectorProductionGA.json.bak $rootDir/Binary/apiservices_dir/InitializationVector.json
    fi
    cp $rootDir/Binary/apiservices.tar.gz $rootDir/Binary/apiservices_dir/package.tar.gz
    runtimeFlags="$runtimeFlags -p 8000:8001 -p 9080:9080 -v $sailDatabaseVolumeName:/srv/mongodb/db0 -v $rootDir/Binary/apiservices_dir:/app $imageName"
elif [ "webfrontend" == "$imageName" ]; then
    make -C $rootDir package_webfrontend -s
    cp webfrontend/InitializationVector.json $rootDir/Binary/webfrontend_dir
    cp $rootDir/Binary/webfrontend.tar.gz $rootDir/Binary/webfrontend_dir/package.tar.gz
    runtimeFlags="$runtimeFlags -p 443:443 -v $rootDir/Binary/webfrontend_dir:/app $imageName"
elif [ "newwebfrontend" == "$imageName" ]; then
    make -C $rootDir package_newwebfrontend -s
    cp newwebfrontend/InitializationVector.json $rootDir/Binary/newwebfrontend_dir
    cp $rootDir/Binary/newwebfrontend.tar.gz $rootDir/Binary/newwebfrontend_dir/package.tar.gz
    runtimeFlags="$runtimeFlags -p 443:443 -v $rootDir/Binary/newwebfrontend_dir:/app $imageName"
elif [ "securecomputationnode" == "$imageName" ]; then
    make -C $rootDir package_securecomputationnode -s
    cp $rootDir/Binary/SecureComputationNode.tar.gz $rootDir/Binary/securecomputationnode_dir/package.tar.gz
    cp securecomputationnode/InitializationVector.json $rootDir/Binary/securecomputationnode_dir
    runtimeFlags="$runtimeFlags -p 3500:3500 -p 6800:6801 -v $rootDir/Binary/securecomputationnode_dir:/app $imageName"
elif [ "rpcrelated" == "$imageName" ]; then
    bash -c "cd $rootDir/RPCLib;./package.sh"
    cp rpcrelated/InitializationVector.json $rootDir/Binary/rpcrelated_dir
    runtimeFlags="$runtimeFlags -p 5556:5556 -p 9090:9091 --cap-add=SYS_ADMIN --cap-add=DAC_READ_SEARCH --privileged -v $rootDir/Binary/rpcrelated_dir:/app $imageName" 
elif [ "auditserver" == "$imageName" ]; then
    runtimeFlags="$runtimeFlags -p 3100:3100 -p 9093:9093 -p 9096:9096 $imageName" 
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
