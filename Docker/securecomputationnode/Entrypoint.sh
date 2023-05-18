#!/bin/bash
set -e
imageName="securecomputationnode"

# cd /app || exit

# Start the nginx server
# nginx -g 'daemon off;' 2>&1 | tee /app/nginx.log &

# mv /decrypt_file.py ./decrypt_file.py

# Use the InitializationVector to get the connection string of the dataset
datasetStoragePassword=$(cat InitializationVector.json | jq -r '.dataset_storage_password')
storageAccountName=$(cat InitializationVector.json | jq -r '.storage_account_name')

# Use the InitializationVector to populate the IP address of the audit services
auditIP=$(cat InitializationVector.json | jq -r '.audit_service_ip')

mountDir="/mnt/azure"
mkdir -p $mountDir

if [ ! -d "/etc/smbcredentials" ]; then
    mkdir /etc/smbcredentials
fi

if [ ! -f "/etc/smbcredentials/$storageAccountName.cred" ]; then
    echo "username=$storageAccountName" >> /etc/smbcredentials/$storageAccountName.cred
    echo "password=$datasetStoragePassword" >> /etc/smbcredentials/$storageAccountName.cred
fi

chmod 600 /etc/smbcredentials/$storageAccountName.cred

# Function that takes in the dataset id, version id and key as arguments and mounts the dataset
mount_datasets() {
  datasetId="$1"
  datasetVersionId="$2"
  datasetKey="$3"
  datasetDir="/data/$datasetId"

  echo "id: $datasetId, version_id: $datasetVersionId"

  echo "//$storageAccountName.file.core.windows.net/$datasetId/$datasetVersionId $mountDir cifs nofail,credentials=/etc/smbcredentials/$storageAccountName.cred,dir_mode=0777,file_mode=0777,serverino,nosharesock,actimeo=30" >> /etc/fstab
  mount -t cifs //$storageAccountName.file.core.windows.net/$datasetId/$datasetVersionId $mountDir -o credentials=/etc/smbcredentials/$storageAccountName.cred,dir_mode=0777,file_mode=0777,serverino,nosharesock,actimeo=30

  # Create a folder for the dataset
  mkdir -p $datasetDir

  # Unzip the dataset_{dataset_version_id} file
  unzip $mountDir/dataset_$datasetVersionId -d $datasetDir

  # Decrypt the dataset_content file
  aesTag=$(cat $datasetDir/dataset_header.json | jq -r '.aes_tag')
  aesNonce=$(cat $datasetDir/dataset_header.json | jq -r '.aes_nonce')

  python3 decrypt_file.py -i $datasetDir/data_content.zip -o $datasetDir/data_content.zip -k $datasetKey -n $aesNonce -t $aesTag
}

# get list of datasets in the InitializationVector
jq -r '.datasets[] | "\(.id) \(.version_id) \(.key)"' < InitializationVector.json |
while read -r id version_id key; do
  # Call the get_data function with the id and version_id values as arguments
  mount_datasets "$id" "$version_id" "$key"
done

jupyter notebook --no-browser --ip 0.0.0.0 --port 8888 --allow-root --NotebookApp.password='argon2:$argon2id$v=19$m=10240,t=10,p=8$CxhdT07OWZQ/VJYTmuT2GA$SFN8uqEKgga19cESOi3jLN5iecshMFPt7BpyHIoL7/g'

# To keep the container running
tail -f /dev/null
