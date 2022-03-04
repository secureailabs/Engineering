#!/bin/bash
# Build SCN Binaries
# Precursor to PackageSecureConputationNode.sh 
set -x

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Build and put stuff in the Binary folder
pushd "$SCRIPT_DIR"/VirtualMachine || exit
for d in $(echo ./*/);do (pushd "$d" || exit; make all -j; popd || exit); done
popd || exit
