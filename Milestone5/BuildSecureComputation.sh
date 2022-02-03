#!/bin/bash
set -x

SCRIPT_DIR=$(pwd)

# Build and put stuff in the Binary folder
pushd "$SCRIPT_DIR"/VirtualMachine || exit
for d in $(echo ./*/);do (pushd "$d" || exit; make all -j; popd || exit); done
popd || exit
