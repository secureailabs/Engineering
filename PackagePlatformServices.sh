#!/bin/bash
# Package Binaries for Platform Services into Tarball
# Postcursor to BuildPlatformServices.sh
# Deployed by DeployPlatform.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if all the required files are present on the machine
declare -a ListOfFiles=(
"Binary/platformservices/RestApiPortal"
"Binary/platformservices/SharedLibraries/RestApiPortal/libSailAuthentication.so"
"Binary/platformservices/SharedLibraries/RestApiPortal/libAzureManager.so"
"Binary/platformservices/SharedLibraries/RestApiPortal/libDatasetFamilyManager.so"
"Binary/platformservices/SharedLibraries/RestApiPortal/libVirtualMachineManager.so"
"Binary/platformservices/SharedLibraries/RestApiPortal/libCryptographicKeyManagement.so"
"Binary/platformservices/SharedLibraries/RestApiPortal/libAuditLogManager.so"
"Binary/platformservices/SharedLibraries/RestApiPortal/libRemoteDataConnectorManager.so"
"Binary/platformservices/SharedLibraries/RestApiPortal/libDatasetDatabase.so"
"Binary/platformservices/SharedLibraries/RestApiPortal/libAccountDatabase.so"
"Binary/platformservices/SharedLibraries/RestApiPortal/libDigitalContractDatabase.so"
"Binary/platformservices/SharedLibraries/RestApiPortal/libDataFederationManager.so"
"Binary/platformservices/Email/main.py"
"Binary/platformservices/Email/sendEmail.py"
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

declare -a ListOfFiles=(
"Binary/dataservices/DatabaseGateway"
"Binary/dataservices/SharedLibraries/DatabasePortal/libDatabaseManager.so"
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
tar -czvf DataServices.tar.gz "${ListOfFiles[@]}"
