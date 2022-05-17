#!/bin/bash
set -e
imageName=apiservices

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
mv InitializationVector.json ApiServices/

if [ -e SecureComputationNode.tar.gz ]
then
    mv SecureComputationNode.tar.gz ApiServices/
fi

# Move the uploaded tool to upload the package and InitializationVector to the SecureComputationNode
mv UploadPackageAndInitializationVector ApiServices/

# Start the local mongodb database
mongod --port 27017 --dbpath /srv/mongodb/db0 --bind_ip localhost --fork --logpath /var/log/mongod.log

# Start the Public API Server
uvicorn app.main:server --reload --host 0.0.0.0 --port 8000

# To keep the container running
tail -f /dev/null
