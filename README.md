[![.github/workflows/build.yml](https://github.com/secureailabs/Engineering/actions/workflows/build.yml/badge.svg)](https://github.com/secureailabs/Engineering/actions/workflows/build.yml)
[![.github/workflows/build.yml](https://github.com/secureailabs/Engineering/actions/workflows/build-c-cpp.yml/badge.svg)](https://github.com/secureailabs/Engineering/actions/workflows/build-c-cpp.yml)
![alt text](https://github.com/secureailabs/Engineering/blob/main/Logo.jpg?raw=true)


# Engineering
This is where the source code for all internal and external facing artifacts get maintained and built.

## Building for source

Open a terminal and clone the git repository:
```sh
$ git clone https://github.com/secureailabs/Engineering.git
```

## For a full end-to-end deployment
Download the datascience repository which is added as a submodule to this repository
```sh
git submodule update --init
```

## Building Binaries
From root of Repository run the following commands to build and verify Binaries

```
make clean
make all -j
```
Outputs:
```
ll -lrt Binary/

## DeployPlatform to Azure
DeployPlatform is required to run behind SAIL VPN. \
Please ensure connection to `vnet-sail-wus-hub-001` and have access to SAIL private vnets in Azure \

Set environment variables in deploy_config.sh to sue `Deploy Platform Service Principal` - Ask Stanley if unclear \
`AZURE_SUBSCRIPTION_ID` should reflect the Azure Subscription you wish to deploy your resources in.
```
export AZURE_SUBSCRIPTION_ID="xxxx"
export AZURE_TENANT_ID="xxxx"
export AZURE_CLIENT_ID="xxxx"
export AZURE_CLIENT_SECRET="xxxx"
export AZURE_OBJECT_ID="xxxx"
export DOCKER_REGISTRY_URL="xxx"
export DOCKER_REGISTRY_USERNAME="xxx"
export DOCKER_REGISTRY_PASSWORD="xxx"
```
One can optionally update the version of the docker container images to be used for deployment by changin the x_TAG variables in deploy_config.sh with the required version.

Run the DeployPlatform script with `--help` for guidance
```
./DeplayPlatform.sh --help
```

## DeployPlatform locally with Docker
There is a readme under `Docker/`
Please see the documentation
