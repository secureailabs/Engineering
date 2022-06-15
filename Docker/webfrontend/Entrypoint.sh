#!/bin/bash
set -e
imageName=webfrontend

cd /app || exit

# Start the nginx server
nginx -g 'daemon off;' 2>&1 | tee /app/nginx.log &

# vm_initializer.py will download the package.tar.gz and InitializationVector.json
# if they are not already present on the file system.
# Forcing a zero exit status as the api server is killed from within and there is no graceful way to do this.
python3 vm_initializer.py || true
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi

# Unpack the tar package
tar -xvf package.tar.gz

# Move the InitializerVector to the Binary folder
mv InitializationVector.json WebFrontend/

# Start the RestApiPortal
cd WebFrontend

# Use the InitializationVector to populate the IP address of the SAIL Platform Services
vmIpAddress=$(cat InitializationVector.json | jq -r '.VirtualMachinePublicIp')
platformServicesUrl=$(cat InitializationVector.json | jq -r '.PlatformServicesUrl')

# Update the client .env file with the Public IP address of the Virtual Machine
pushd client
sed -i "s,https:\/\/127\.0\.0\.1:3000,$vmIpAddress,g" .env
popd

# Update the server .env file with the Public IP address of the SAIL Platform Services
pushd server
sed -i "s,https:\/\/backend:6200,$platformServicesUrl,g" .env
sed -i "s,https:\/\/127\.0\.0\.1:3000,$vmIpAddress,g" .env
popd

# Build and run the frontend application
yarn --cwd client install && yarn cache clean && yarn --cwd client build
yarn --cwd server install && yarn cache clean

chmod +x env.sh
./env.sh && yarn --cwd /app/WebFrontend/server prod && /bin/bash
