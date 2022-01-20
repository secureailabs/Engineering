#!/bin/bash

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
    find Binary | grep -x $val
    retVal=$?
    if [ $retVal -ne 0 ]; then
        echo "Error ${val} does not exist"
        exit $retVal
    fi
done

set -e
# Compress and package all the files
tar -czvf SecureComputationNode.tar.gz "${ListOfFiles[@]}"

echo "Success!!"
