# Managed Images using Packer

## Install Packer
```
curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -
apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
apt-get update && apt-get install -y packer
```
## Install Node and Dependencies
```
# Using Ubuntu
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v # v18.5.0
npm -v # 8.12.1
npm install --save-dev senv
```
### Decrypt [.env.dev.encrypted]
In your local environment set `DOTENV_PASS=`[GITHUB.env.pass](https://start.1password.com/open/i?a=VDKXP5MBWJAW3F3YRPJNHPGKLM&v=gy4saia7pduzqbp7qhij776a4u&i=kmdczi5wvgpty6kqodhjdjyydy&h=secureailabs.1password.com) \
Run the Following command to optain a decrypted .env.dev file.
```
npm run env:decrypt # You should obtain .env.dev under this directory
```
`.env.dev` contains `AZURE_CLIENT_ID`  which is set for PACKER Azure Service principal - Ask Stanley if unclear
### Update .envs' should be Encrypted [.env.dev]
**PLEASE REMEMBER: Not to commit .envs that aren't encrypted**
```
npm run env:encrypt # You should obtain .env.dev.encrypted under this directory
```
## Run image create script
Run the AzureImageCreate.sh script to build VM images which is a two step process.
First it will create a VHD image using packer and then there is a manual process to convert that image to a managed image.
where the user needs to copy the vhd image url and paste it as a user input in the terminal when asked for.

## Requirements
`../../Binary/vm_initializer.py` should exist before running this script which can be created by running `make all` in the `VirtualMachine/VmInitializer` directory.
