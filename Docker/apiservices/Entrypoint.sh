#!/bin/bash
set -e
imageName=apiservices

cd /app || exit

# Start the nginx server
nginx -g 'daemon off;' 2>&1 | tee /app/nginx.log &

# vm_initializer will download the package.tar.gz and InitializationVector.json
# if they are not already present on the file system.
# Forcing a zero exit status as the api server is killed from within and there is no graceful way to do this.
python3 vm_initializer.py || true
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi

# Unpack the tar package
tar -xf package.tar.gz

# Use the InitializationVector to populate the IP address of the audit services
auditEndpoint=$(cat InitializationVector.json | jq -r '.audit_service_endpoint')

# Move the InitializerVector to the Binary folder
mv InitializationVector.json ApiServices/

# Start the local mongodb database
mongod --port 27017 --dbpath /srv/mongodb/db0 --bind_ip localhost --fork --logpath /var/log/mongod.log

# modify the audit service ip of promtail config file
sed -i "s,http\:\/\/auditserver\:3100\/loki\/api\/v1\/push,$auditEndpoint,g" /promtail_local_config.yaml

# Start the promtail client
/promtail_linux_amd64 -config.file=/promtail_local_config.yaml  > /promtail.log 2>&1&

# Start the Public API Server
cd ApiServices
uvicorn app.main:server --host 0.0.0.0 --port 8000 --workers 4

# To keep the container running
tail -f /dev/null
