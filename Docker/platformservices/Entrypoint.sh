#!/bin/bash
set -e
imageName=platformservices

cd /app || exit

# Start the nginx server
nginx -g 'daemon off;' 2>&1 | tee /app/nginx.log &

# BaseVmImageInit will download the package.tar.gz and InitializationVector.json
# if they are not already present on the file system.
./BaseVmImageInit
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi

# Unpack the tar package
tar -xvf package.tar.gz

# Move the InitializerVector to the Binary folder
mv InitializationVector.json Binary/$imageName/

# Start the RestApiPortal
cd Binary/$imageName
./RestApiPortal 2>&1 | tee restportal.log &

# Start the Email Plugin
pushd Email
uvicorn main:emailPlugin --host 0.0.0.0 2>&1 | tee email.log &
popd

# To keep the container running
tail -f /dev/null
