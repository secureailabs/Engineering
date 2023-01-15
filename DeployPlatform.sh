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

# Install build tools
./install.sh

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

# Check for Azure environment variables
if [ -z "${AZURE_SUBSCRIPTION_ID}" ]; then
  echo "environment variable AZURE_SUBSCRIPTION_ID is undefined"
  exit 1
fi
if [ -z "${AZURE_TENANT_ID}" ]; then
  echo "environment variable AZURE_TENANT_ID is undefined"
  exit 1
fi
if [ -z "${AZURE_CLIENT_ID}" ]; then
  echo "environment variable AZURE_CLIENT_ID is undefined"
  exit 1
fi
if [ -z "${AZURE_CLIENT_SECRET}" ]; then
  echo "environment variable AZURE_CLIENT_SECRET is undefined"
  exit 1
fi
if [ -z "${AZURE_OBJECT_ID}" ]; then
  echo "environment variable AZURE_OBJECT_ID is undefined"
  exit 1
fi

# Build and Package the Platform Services
make package_apiservices
make sail_client database_initializer
make databaseInitializationTool
make package_newwebfrontend
make package_audit_service

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

# TODO: Prawal. This is a temporary fix. Ideally the initializationVector should be generated at runtime
cp Docker/apiservices/InitializationVector.json $tempDeployDir/apiservices.json
cp Docker/apiservices/InitializationVector.json $tempDeployDir/auditserver.json

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
  --env AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID \
  --env AZURE_TENANT_ID=$AZURE_TENANT_ID \
  --env AZURE_CLIENT_ID=$AZURE_CLIENT_ID \
  --env AZURE_CLIENT_SECRET=$AZURE_CLIENT_SECRET \
  --env AZURE_OBJECT_ID=$AZURE_OBJECT_ID \
  --env VERSION=$gitCommitId \
  --env PUBLIC_IP=$PUBLIC_IP \
  azuredeploymenttools
popd

# Cleanup the temporary directory
rm -rf $tempDeployDir
