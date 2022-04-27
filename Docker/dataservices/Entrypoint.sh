#!/bin/bash
set -e
imageName=dataservices

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

# Comment the following line if the mongodb atlas is to be used instead of local mongo installation
mongod --port 27017 --dbpath /srv/mongodb/db0 --replSet rs0 --bind_ip localhost --fork --logpath /var/log/mongod.log
./DatabaseGateway 2>&1 | tee databasegateway.log &
tail -f /dev/null
