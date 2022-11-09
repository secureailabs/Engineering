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

# Use the InitializationVector to get the connection string of the dataset
datasetStoragePassword=$(cat InitializationVector.json | jq -r '.dataset_storage_password')
storageAccountName=$(cat InitializationVector.json | jq -r '.storage_account_name')
datasetVersionId=$(cat InitializationVector.json | jq -r '.dataset_version_id')
datasetId=$(cat InitializationVector.json | jq -r '.dataset_id')
datasetKey=$(cat InitializationVector.json | jq -r '.dataset_key')

mountDir="/mnt/azure"
ls -l $mountDir
mkdir -p $mountDir
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
mkdir -p /data

# Unzip the dataset_{dataset_version_id} file
unzip $mountDir/dataset_$datasetVersionId -d /data

# Unzip the dataset_model zip file
mkdir -p /data/data_model
unzip /data/data_model.zip -d /data/data_model
rm -rf /data/data_model.zip

# Decrypt the dataset_content file
aesTag=$(cat /data/dataset_header.json | jq -r '.aes_tag')
aesNonce=$(cat /data/dataset_header.json | jq -r '.aes_nonce')
python3 decrypt_file.py -i /data/data_content.zip -o /data/data_content.zip -k $datasetKey -n $aesNonce -t $aesTag

# Unzip the dataset_content zip file
mkdir -p /data/data_content
unzip /data/data_content.zip -d /data/data_content
rm -rf /data/data_content.zip

# Install the rpc library
pip3 install /app/zero
pip3 install /app/datascience/sail-safe-functions

# Start the rpc server
python3 /app/test_server.py 5556

# To keep the container running
tail -f /dev/null
