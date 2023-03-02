#!/bin/bash
set -e
set -x

PrintHelp()
{
    echo ""
    echo "Usage: $0 -p [Purpose:[Nightly, Bugfix, etc..]] -o [Owner: [Prawal, Stanley]]"
    echo -e "\t-p Purpose: purpose of deployment. No spaces. "
    echo -e "\t-o Triggered By: deployment owner name. No spaces."
    exit 1 # Exit script after printing help
}

# Check if docker is installed
docker --version
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error docker does not exist"
    exit $retVal
fi

# the default value for the docker is false
docker="true"

# Parse the input parameters
while getopts "p:o:c" opt
do
    echo "opt: $opt $OPTARG"
    case "$opt" in
        p ) purpose="$OPTARG" ;;
        o ) owner="$OPTARG" ;;
        c ) docker="false" ;;
        ? ) PrintHelp ;;
    esac
done

# Print Help in case parameters are not correct
if [ -z "$purpose" ] || [ -z "$owner" ]
then
    PrintHelp
fi
echo "Purpose: $purpose"
echo "Owner: $owner"

# Get short git commit id
if [ -z "$GIT_COMMIT" ]; then
    gitCommitId=$(git rev-parse --short HEAD)
else
    gitCommitId=$GIT_COMMIT
fi

# Check for CI
if [ "$docker" = "true" ]; then
    echo "Running on local machine"
    docker run -it -v $(pwd):/app --env OWNER=$owner --env PURPOSE=$purpose --env GIT_COMMIT=$gitCommitId --entrypoint="/app/DeployPlatform/entrypoint.sh" developmentdockerregistry.azurecr.io/ciubuntu:v0.1.0_5f85ced
    exit 0
fi

# Make sure the user is logged in to docker
export tempDeployDir=$(mktemp -d --tmpdir=.)

# Build and Package the Platform Services
make package_audit_service
make package_apiservices
make sail_client database_initializer
#make package_newwebfrontend

# Create a temporary directory to store the files
mkdir -p $tempDeployDir

# Copy the files to the temporary directory
cp -r AzureDeploymentTemplates/ArmTemplates $tempDeployDir
# cp Binary/newwebfrontend.tar.gz $tempDeployDir
cp ApiServices/generated/sail-client/dist/sail_client-0.1.0-py3-none-any.whl $tempDeployDir
cp database-initialization/dist/database_initialization-0.1.0-py3-none-any.whl $tempDeployDir

cp Binary/apiservices.tar.gz $tempDeployDir/apiservices.tar.gz
cp -r DeployPlatform/* $tempDeployDir
cp Binary/auditserver.tar.gz $tempDeployDir

# TODO: This is a temporary fix. Ideally the initializationVector should be generated at runtime
cp Docker/apiservices/InitializationVector.json $tempDeployDir/apiservices.json
cp Docker/apiservices/InitializationVector.json $tempDeployDir/auditserver.json

# Copy the configuration file
cp deploy_config.sh $tempDeployDir

# Run the docker image to deploy the application on the Azure
export OWNER=$owner
export PURPOSE=$purpose
export VERSION=$gitCommitId
export PUBLIC_IP=$PUBLIC_IP

# Build the docker image
pushd $tempDeployDir
pip3 install sail_client-0.1.0-py3-none-any.whl
pip3 install database_initialization-0.1.0-py3-none-any.whl

source deploy_config.sh
python3 Deploy.py
popd

# Cleanup the temporary directory
rm -rf $tempDeployDir
