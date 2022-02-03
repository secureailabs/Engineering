#!/bin/bash

cd /app || exit

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

chmod +x /app/env.sh
/app/env.sh && yarn --cwd /app/server prod && /bin/bash
