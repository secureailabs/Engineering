#!/bin/bash
set -e
imageName=auditserver

cd /app || exit

# Start the nginx server
nginx -g 'daemon off;' 2>&1 | tee /app/nginx.log &

# vm_initializer will download the package.tar.gz and InitializationVector.json
# if they are not already present on the file system.
# Forcing a zero exit status as the api server is killed from within and there is no graceful way to do this.
mv /vm_initializer.py ./vm_initializer.py
python3 vm_initializer.py || true
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi

# Unpack the tar package
tar -xf package.tar.gz

# Use the InitializationVector to populate the parameters of the audit services
export auditStorageAccountName=$(cat InitializationVector.json | jq -r '.azure_storage_account_name')
export auditTenantID=$(cat InitializationVector.json | jq -r '.azure_tenant_id')
export auditClientID=$(cat InitializationVector.json | jq -r '.azure_client_id')
export auditClientSecret=$(cat InitializationVector.json | jq -r '.azure_client_secret')

# Populate the parameters into yaml config file
yq -i '.storage_config.azure.account_name=env(auditStorageAccountName)' ./AuditService/loki_local_config.yaml
yq -i '.storage_config.azure.tenant_id=env(auditTenantID)' ./AuditService/loki_local_config.yaml
yq -i '.storage_config.azure.client_id=env(auditClientID)' ./AuditService/loki_local_config.yaml
yq -i '.storage_config.azure.client_secret=env(auditClientSecret)' ./AuditService/loki_local_config.yaml

# initialize the loki server
./AuditService/loki_linux_amd64 -config.file=./AuditService/loki_local_config.yaml
