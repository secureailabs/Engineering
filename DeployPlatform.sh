#!/bin/bash
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

# Build and Package the Platform Services
make package_apiservices -j
make databaseInitializationTool -j
make package_newwebfrontend -j

# Create a temporary directory to store the files
mkdir -p $tempDeployDir

# Copy the files to the temporary directory
cp Binary/DatabaseInitializationTool $tempDeployDir
cp Binary/igr_001.csvp $tempDeployDir
cp Binary/igr_002.csvp $tempDeployDir
cp Binary/mgr_001.csvp $tempDeployDir
cp Binary/DatabaseInitializationSettings.json $tempDeployDir
cp Binary/UploadPackageAndInitializationVector $tempDeployDir
cp -r AzureDeploymentTemplates/ArmTemplates $tempDeployDir
mv Binary/newwebfrontend.tar.gz $tempDeployDir
cp Binary/apiservices.tar.gz $tempDeployDir/apiservices.tar.gz
cp -r InternalTools/DeployPlatform/* $tempDeployDir

# TODO: Prawal. This is a temporary fix. Ideally the initializationVector should be generated at runtime
cp Docker/apiservices/InitializationVector.json $tempDeployDir/apiservices.json

# Check for the docker image and create it if it does not exist
docker images | grep -x "azuredeploymenttools"
retVal=$?
if [ $retVal -ne 0 ]; then
  echo "Error: Docker image not found"
  pushd $tempDeployDir
  docker build -t azuredeploymenttools .
  popd
fi

# Run the docker image to deploy the application on the Azure
pushd $tempDeployDir
docker run \
  -it \
  -v $(pwd):/app \
  --env AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID \
  --env AZURE_TENANT_ID=$AZURE_TENANT_ID \
  --env AZURE_CLIENT_ID=$AZURE_CLIENT_ID \
  --env AZURE_CLIENT_SECRET=$AZURE_CLIENT_SECRET \
  --env OWNER=$owner \
  --env PURPOSE=$purpose \
  azuredeploymenttools
popd

# Cleanup the temporary directory
rm -rf $tempDeployDir
