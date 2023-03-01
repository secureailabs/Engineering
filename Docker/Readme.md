# Readme

## Pre-requirements
### Clone down datascience repo as submodule
```
cd Engineering/
git submodule update --init
```

## Build all the docker images
```
./BuildImage.sh
```

## Build and push docker images
Before you can push the images to the docker hub, you need to login az cli and set the subscription to the one that has the docker hub registry.

```
az login --service-principal --username $AZURE_CLIENT_ID --password $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
az account set --subscription $AZURE_SUBSCRIPTION_ID
# set the docker hub registry, use the one provided or whatever is relevant
export DOCKER_REGISTRY_NAME="developmentdockerregistry"
./BuildImage.sh -i <image_name> -p
```

## Run the services

### Backend Api Services Portal
```
./RunService.sh -s apiservices
```
### Web Frontend
```
./RunService.sh -s newwebfrontend
```
### RPC server
```
./RunService.sh -s rpcrelated
```
### Audit server
```
./RunService.sh -s auditserver
```
### Shutdown and Deprovision services

#### All Docker
```
./DeprovisionService.sh -s all
```
*Alternatively, you can add DeprovisionService.sh to path via symbolic link and trigger from anywhere!*
```
eg:
echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/bin
cd /bin
ln -s <abs_path>/Engineering/Docker/DeprovisionService.sh .
DeprovisionService.sh -s all
```

#### Platformservices
```
./DeprovisionService.sh -s apiservices
```
#### Web Frontend
```
./DeprovisionService.sh -s newwebfrontend
```
### RPC Server
```
./DeprovisionService.sh -s rpcrelated
```
### Audit Server
```
./DeprovisionService.sh -s auditserver
```
#### Note:
1. Use the `-d` flag to run the services in the background in docker detached mode.
2. To access the backend portal from any other container use `apiservices` as a domain name. e.g. the frontend webApp must connect to `https://apiservices:6200` instead of `https://127.0.0.1:6200/`
3. Remember you can add DeprovisionService.sh to path and run it from anywhere !!  via `DeprovisionService.sh -s all`
