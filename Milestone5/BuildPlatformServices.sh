#!/bin/bash
# Build Binaries for Platform Services
# Precursor to PackagePlatformServices.sh
# Deployed by DeployPlatform.sh
set -e
set -x

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Build and put stuff in the Binary folder
pushd "${SCRIPT_DIR}/WebService/RestApiPortal"
make all -j
popd

pushd "${SCRIPT_DIR}/WebService/DatabaseGateway"
make all -j
popd

pushd "${SCRIPT_DIR}/WebService/Plugins/RestApiPortal"
for d in $(echo ./*/);do (pushd "$d"; make all -j; popd); done
popd

pushd "${SCRIPT_DIR}\/WebService/Plugins/DatabasePortal"
for d in $(echo ./*/);do (cd "$d"; make all -j; popd); done
popd
