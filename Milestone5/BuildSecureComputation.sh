#!/bin/bash
set -x

SCRIPT_DIR=$(pwd)

# Build and put stuff in the Binary folder
pushd $SCRIPT_DIR/VirtualMachine
for d in $(echo ./*/);do (pushd $d; make all -j; popd); done
popd
