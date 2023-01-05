# Managed Images using Packer

> ## PREREQISITE REQUIREMENTS
`../../Binary/vm_initializer.py` should exist before running this script which can be created by running `make all` in the `VirtualMachine/VmInitializer` directory.

> ### Install AZURE CLI
https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt

> ### Install Packer
```
curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -
apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
apt-get update && apt-get install -y packer
```

> ### Install Node and Dependencies
```
# Using Ubuntu
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v # v18.5.0
npm -v # 8.12.1
npm install --save-dev senv
```

> ### SET Azure Service Principals
Find `PACKER` service principal in `Projects` vault within 1Password
Export found values
```
export AZURE_SUBSCRIPTION_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export AZURE_TENANT_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export AZURE_CLIENT_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export AZURE_CLIENT_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

--------------------------------------------------------------------------------------------------
> ## Run image create script
Run the AzureImageCreate.sh script to build VM images which is a two step process. \
First it will create a VHD image using packer and then there is a manual process to convert that image to a managed image. \
Manual execution: `./AzureImageCreate.sh -m <IMAGE_NAME>` \
Automated execution used by CI : `./AzureImageCreate.sh -a -m <IMAGE_NAME>`

