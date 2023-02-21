#!/bin/bash
set -e
set -x

export tempDeployDir=$(mktemp -d --tmpdir=.)

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

# Parse the input parameters
while getopts "p:o:" opt
do
    echo "opt: $opt $OPTARG"
    case "$opt" in
        p ) purpose="$OPTARG" ;;
        o ) owner="$OPTARG" ;;
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

# Build the docker image
pushd $tempDeployDir
docker build -t azuredeploymenttools .
popd

# Get short git commit id
gitCommitId=$(git rev-parse --short HEAD)

# Run the docker image to deploy the application on the Azure
pushd $tempDeployDir
docker run \
  -t \
  -v $(pwd):/app \
  --env OWNER=$owner \
  --env PURPOSE=$purpose \
  --env VERSION=$gitCommitId \
  --env PUBLIC_IP=$PUBLIC_IP \
  azuredeploymenttools
popd

# Cleanup the temporary directory
rm -rf $tempDeployDir
