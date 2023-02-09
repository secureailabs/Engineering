#!/bin/bash
set -e
imageName=rpcrelated

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
tar -xvf package.tar.gz
ls /app
# Move the DS Library to /ds
mv /app/datascience /ds

# Use the InitializationVector to get the connection string of the dataset
datasetStoragePassword=$(cat InitializationVector.json | jq -r '.dataset_storage_password')
storageAccountName=$(cat InitializationVector.json | jq -r '.storage_account_name')
datasetVersionId=$(cat InitializationVector.json | jq -r '.dataset_version_id')
datasetId=$(cat InitializationVector.json | jq -r '.dataset_id')

localDataset=$(cat InitializationVector.json | jq -r '.local_dataset')
if [ "$localDataset" = "null" ]; then
    localDataset=false
fi

# Use the InitializationVector to populate the IP address of the audit services
auditIP=$(cat InitializationVector.json | jq -r '.audit_service_ip')

# modify the audit service ip of promtail config file
sed -i "s,auditserver,$auditIP,g" /app/RPCLib/promtail_local_config.yaml

mountDir="/mnt/azure"
datasetDir="/data/$datasetId"
mkdir -p $mountDir

if $localDataset; then
    echo "Using local dataset: $datasetVersionId"
    ls /
    ls /local_dataset/
    unzip /local_dataset/$datasetVersionId -d /data
    ls /data
else
    if [ ! -d "/etc/smbcredentials" ]; then
        mkdir /etc/smbcredentials
    fi

    if [ ! -f "/etc/smbcredentials/$storageAccountName.cred" ]; then
        echo "username=$storageAccountName" >> /etc/smbcredentials/$storageAccountName.cred
        echo "password=$datasetStoragePassword" >> /etc/smbcredentials/$storageAccountName.cred
    fi

    chmod 600 /etc/smbcredentials/$storageAccountName.cred
    echo "//$storageAccountName.file.core.windows.net/$datasetId/$datasetVersionId $mountDir cifs nofail,credentials=/etc/smbcredentials/$storageAccountName.cred,dir_mode=0777,file_mode=0777,serverino,nosharesock,actimeo=30" >> /etc/fstab
    mount -t cifs //$storageAccountName.file.core.windows.net/$datasetId/$datasetVersionId $mountDir -o credentials=/etc/smbcredentials/$storageAccountName.cred,dir_mode=0777,file_mode=0777,serverino,nosharesock,actimeo=30

    # Create a folder for the dataset
    mkdir -p $datasetDir

    # Unzip the dataset_{dataset_version_id} file
    unzip $mountDir/dataset_$datasetVersionId -d $datasetDir

    # Decrypt the dataset_content file
    aesTag=$(cat $datasetDir/dataset_header.json | jq -r '.aes_tag')
    aesNonce=$(cat $datasetDir/dataset_header.json | jq -r '.aes_nonce')
    datasetKey=$(cat InitializationVector.json | jq -r '.dataset_key')
    python3 decrypt_file.py -i $datasetDir/data_content.zip -o $datasetDir/data_content.zip -k $datasetKey -n $aesNonce -t $aesTag
fi

# Install the rpc library
pip3 install /app/RPCLib/zero
pip3 install -e /ds/sail-core
pip3 install -e /ds/sail-safe-functions

# Set Environment variables
export PATH_DIR_PUBLIC_KEY_ZEROMQ="/app/RPCLib/public_keys/"
export PATH_FILE_PRIVATE_KEY_ZEROMQ_CLIENT="/app/RPCLib/private_keys/client.key_secret"
export PATH_FILE_PRIVATE_KEY_ZEROMQ_SERVER="/app/RPCLib/private_keys/server.key_secret"
export PATH_DIR_DATASET="/data/"

# Start the promtail client
/app/RPCLib/promtail_linux_amd64 -config.file=/app/RPCLib/promtail_local_config.yaml  > /app/promtail.log 2>&1&

# Start the rpc server
python3 /ds/sail-participant-zeromq/server.py 5556

# To keep the container running
tail -f /dev/null
