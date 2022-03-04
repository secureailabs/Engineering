#!/bin/bash
# Package Binaries for Web Front End into Tarball
# Deployed by DeployPlatform.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

pushd "${SCRIPT_DIR}/WebFrontend/client" || exit
rm -rf node_modules
popd || exit

pushd "${SCRIPT_DIR}/WebFrontend/server" || exit
rm -rf node_modules
popd || exit

# Compress and package all the files
cd "${SCRIPT_DIR}" || exit
tar -czvf webfrontend.tar.gz WebFrontend
