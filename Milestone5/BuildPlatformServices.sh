#!/bin/bash
set -e
set -x

SCRIPT_DIR=$(pwd)

# Build and put stuff in the Binary folder
pushd $SCRIPT_DIR/WebService/RestApiPortal
make all -j
popd

pushd $SCRIPT_DIR/WebService/DatabaseGateway
make all -j
popd

pushd $SCRIPT_DIR/WebService/Plugins/RestApiPortal
for d in $(echo ./*/);do (pushd $d; make all -j; popd); done
popd

pushd $SCRIPT_DIR/WebService/Plugins/DatabasePortal
for d in $(echo ./*/);do (cd $d; make all -j; popd); done
popd
