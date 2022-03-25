#!/bin/bash
# set -e
declare -a StringArray=("BaseVmImageInit" "CommunicationPortal" "DataDomainProcess"
"DatabaseTools" "InitializerProcess" "JobEngine" "RootOfTrustProcess" "SignalTerminationProcess"
"Tests")

declare -a StringArray2=("DatabaseGateway" "RestApiPortal" "libDatabaseManager.so" "libAccountDatabase.so" "libAuditLogManager.so" "libAzureManager.so"
"libCryptographicKeyManagement.so" "libDatasetDatabase.so" "libDigitalContractDatabase.so"
"libRemoteDataConnectorManager.so" "libSailAuthentication.so" "libVirtualMachineManager.so"
"libDatasetFamilyManager.so" "libDataFederationManager.so" "SAILPyAPI.so")

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
set -x

# Build and put stuff in the Binary folder
cd "$SCRIPT_DIR"/WebService/Plugins/RestApiPortal
for d in $(echo ./*/);do (cd "$d"; make all -j && returncode=$? || returncode=$?; cd ..); done

cd "$SCRIPT_DIR"/WebService/Plugins/DatabasePortal
for d in $(echo ./*/);do (cd "$d"; make all -j && returncode=$? || returncode=$?; cd ..); done

cd "$SCRIPT_DIR"/VirtualMachine
for d in $(echo ./*/);do (cd "$d"; make all -j && returncode=$? || returncode=$?; cd ..); done

cd "$SCRIPT_DIR"/WebService
for d in $(echo ./*/);do (cd "$d"; make all -j && returncode=$? || returncode=$?; cd ..); done

cd "$SCRIPT_DIR"/EndPointTools
for d in $(echo ./*/);do (cd "$d"; make all -j && returncode=$? || returncode=$?; cd ..); done

cd "$SCRIPT_DIR"/InternalTools/DatabaseTools/
make all -j && returncode=$? || returncode=$?

set +x
# Verify files exists
for val in "${StringArray[@]}"; do
    echo -e "\nsearching for ${val} ..."
    ls -rt "$SCRIPT_DIR"/Binary/ | grep "$val"
    retVal=$?
    if [ $retVal -ne 0 ]; then
        echo "Error ${val} does not exist"
        exit $retVal
    fi
done

# Verify .so files exists
for val in "${StringArray2[@]}"; do
    echo -e "\nsearching for ${val} ..."
    ls -Rt "$SCRIPT_DIR"/Binary/ | grep "$val"
    retVal=$?
    if [ $retVal -ne 0 ]; then
        echo "Error ${val} does not exist"
        exit $retVal
    fi
done
set -e