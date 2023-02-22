# Managed Images using Packer

> ### Install AZURE CLI
https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt

> ### Install Packer
```
curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -
apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
apt-get update && apt-get install -y packer
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
Run the AzureImageCreate.sh script to build VM images
