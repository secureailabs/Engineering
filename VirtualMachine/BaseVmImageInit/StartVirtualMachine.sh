#!/bin/bash
set -e

# BaseVmImageInit will download the package.tar.gz and InitializationVector.json
# if they are not already present on the file system.
./BaseVmImageInit
retVal=$?

if [ $retVal -ne 0 ]; then
    exit $retVal
fi

# Unpack the tar package
tar -xvf package.tar.gz

# Run the docker container
./Run.sh
