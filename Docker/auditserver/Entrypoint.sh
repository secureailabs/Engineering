#!/bin/bash
set -e
imageName=auditserver

cd /app

# Use the InitializationVector to populate the parameters of the audit services
export auditStorageAccountName=$(cat InitializationVector.json | jq -r '.azure_storage_account_name')
export auditTenantID=$(cat InitializationVector.json | jq -r '.azure_tenant_id')
export auditClientID=$(cat InitializationVector.json | jq -r '.azure_client_id')
export auditClientSecret=$(cat InitializationVector.json | jq -r '.azure_client_secret')

# Populate the parameters into yaml config file
yq -i '.storage_config.azure.account_name=env(auditStorageAccountName)' ./loki_local_config.yaml
yq -i '.storage_config.azure.tenant_id=env(auditTenantID)' ./loki_local_config.yaml
yq -i '.storage_config.azure.client_id=env(auditClientID)' ./loki_local_config.yaml
yq -i '.storage_config.azure.client_secret=env(auditClientSecret)' ./loki_local_config.yaml

# initialize the loki server
./loki_linux_amd64 -config.file=./loki_local_config.yaml
