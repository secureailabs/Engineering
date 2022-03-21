#!/bin/bash
# Package Binaries for SCN into Tarball
# During SCN deployment: will first check locally in Binary/ for Tarball before attempting through Azure
# If you want a SCN built from your local repo via docker copy Tarball into Binary/

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if all the required files are present on the machine
declare -a ListOfFiles=(
"Binary/RootOfTrustProcess"
"Binary/CommunicationPortal"
"Binary/InitializerProcess"
"Binary/SignalTerminationProcess"
"Binary/DataDomainProcess"
"Binary/JobEngine"
"Binary/PrivacySentinel.py"
"Binary/PrivacySentinelPolicy.json"
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
tar -czvf SecureComputationNode.tar.gz "${ListOfFiles[@]}"

echo "Success!!"
