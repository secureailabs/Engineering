#!/bin/bash
# Package Binaries for Platform Services into Tarball
# Postcursor to BuildPlatformServices.sh
# Deployed by DeployPlatform.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if all the required files are present on the machine
declare -a ListOfFiles=(
"Binary/DatabaseGateway"
"Binary/RestApiPortal"
"Binary/SharedLibraries/DatabasePortal/libDatabaseManager.so"
"Binary/SharedLibraries/RestApiPortal/libSailAuthentication.so"
"Binary/SharedLibraries/RestApiPortal/libAzureManager.so"
"Binary/SharedLibraries/RestApiPortal/libDatasetFamilyManager.so"
"Binary/SharedLibraries/RestApiPortal/libVirtualMachineManager.so"
"Binary/SharedLibraries/RestApiPortal/libCryptographicKeyManagement.so"
"Binary/SharedLibraries/RestApiPortal/libAuditLogManager.so"
"Binary/SharedLibraries/RestApiPortal/libRemoteDataConnectorManager.so"
"Binary/SharedLibraries/RestApiPortal/libDatasetDatabase.so"
"Binary/SharedLibraries/RestApiPortal/libAccountDatabase.so"
"Binary/SharedLibraries/RestApiPortal/libDigitalContractDatabase.so"
"Binary/SharedLibraries/RestApiPortal/libDataFederationManager.so"
)

for val in "${ListOfFiles[@]}"; do
    echo -e "\nSearching for ${val} ..."
    find "${SCRIPT_DIR}/Binary" | grep -x "${SCRIPT_DIR}/${val}"
    retVal=$?
    if [ $retVal -ne 0 ]; then
        echo "Error ${val} does not exist"
        exit $retVal
    fi
done

set -e
# Compress and package all the files
cd "${SCRIPT_DIR}"
tar -czvf PlatformServices.tar.gz "${ListOfFiles[@]}"

echo "Success!!"
