#!/bin/bash
set -e
set -x
create_docker_flag="true"

PrintHelp()
{
    echo ""
    echo "Usage: $0 -p [Purpose:[Nightly, Bugfix, etc..]] -o [Owner: [Prawal, Stanley]]"
    echo -e "\t-p Purpose: purpose of deployment. No spaces. "
    echo -e "\t-o Triggered By: deployment owner name. No spaces."
    echo -e "\t-c Create_docker_flag; Flag used by CI for specifying currently executing script via docker on host machine"
    exit 1 # Exit script after printing help
}

# Check if docker is installed
docker --version
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error docker is not installed; please install before continuing"
    exit $retVal
fi

# Parse the input parameters
while getopts "p:o:c" opt
do
    echo "opt: $opt $OPTARG"
    case "$opt" in
        p ) purpose="$OPTARG" ;;
        o ) owner="$OPTARG" ;;
        c ) create_docker_flag="false" ;;
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
echo "docker_flag: $docker_flag"

# Get short git commit id
if [ -z "$GIT_COMMIT" ]; then
    gitCommitId=$(git rev-parse --short HEAD)
else
    gitCommitId=$GIT_COMMIT
fi

# Check for whether script was started via manual run of bash script
if [ "$create_docker_flag" = "true" ]; then
    echo "Start docker container on local machine to run DeployPlatform.sh"
    docker run -it -v $(pwd):/app -w /app --env OWNER=$owner --env PURPOSE=$purpose --env GIT_COMMIT=$gitCommitId --entrypoint="/app/Docker/ci_deploy_platform/Entrypoint.sh" developmentdockerregistry.azurecr.io/ciubuntu:v0.1.0_5f85ced
    exit 0
fi

#
# The following lines are all run on docker container developmentdockerregistry.azurecr.io/ciubuntu
#

# Create a temporary directory to store the files
export tempDeployDir=$(mktemp -d --tmpdir=.)
mkdir -p $tempDeployDir

# Build and Package the Platform Services
make package_audit_service
make sail_client database_initializer
#make package_newwebfrontend

# Copy the files to the temporary directory
cp -r AzureDeploymentTemplates/ArmTemplates $tempDeployDir
# cp Binary/newwebfrontend.tar.gz $tempDeployDir
cp ApiServices/generated/sail-client/dist/sail_client-0.1.0-py3-none-any.whl $tempDeployDir
cp database-initialization/dist/database_initialization-0.1.0-py3-none-any.whl $tempDeployDir
cp -r DeployPlatform/* $tempDeployDir
cp Binary/auditserver.tar.gz $tempDeployDir

# Copy the configuration file
cp deploy_config.sh $tempDeployDir
# Run the docker image to deploy the application on the Azure
export OWNER=$owner
export PURPOSE=$purpose
export VERSION=$gitCommitId
export PUBLIC_IP=$PUBLIC_IP
# Install additional dependencies for Deploy.py
pushd $tempDeployDir
pip3 install sail_client-0.1.0-py3-none-any.whl
pip3 install database_initialization-0.1.0-py3-none-any.whl
# Run Deploy script
source deploy_config.sh
python3 Deploy.py
popd

# Cleanup the temporary directory
rm -rf $tempDeployDir
