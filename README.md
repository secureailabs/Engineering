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
git submodule update
```

## Building Binaries
From root of Repository run the following commands to build and verify Binaries

**Linux**
```
make clean
make all -j
```
Outputs:
```
ll -lrt Binary/
```

**Windows**
```
.\Manual-WindowsPlatformDeliverables.bat
```
Ouputs:
```
WindowsPlatformDeliverables.tar
```

## DeployPlatform to Azure
Set environment variables to use `Deploy Platform Service Principal` - Ask Stanley if unclear \
`AZURE_SUBSCRIPTION_ID` should reflect the Azure Subscription you wish to deploy your resources in.
```
export AZURE_SUBSCRIPTION_ID="xxxx"
export AZURE_TENANT_ID="xxxx"
export AZURE_CLIENT_ID="xxxx"
export AZURE_CLIENT_SECRET="xxxx"
```
Run the DeployPlatform script with `--help` for guidance
```
./DeplayPlatform.sh --help
```

## DeployPlatform locally with Docker
There is a readme under `Docker/`
Please see the documentation
