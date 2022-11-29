# Readme

## Pre-requirements
### Remake Binaries

Go to Engineering/
```
make clean

make all -j 
```

## Build all the docker images
```
./BuildImage.sh
```

## Run the services

### Backend Api Services Portal
```
./RunService.sh -s apiservices
```
### Orchestrator
```
./RunService.sh -s orchestrator
```
### Remote Data Connector
```
./RunService.sh -s remoteDataConnector
```

### Secure Computation Node
```
./RunService.sh -s securecomputationnode
```
### Web Frontend
```
./RunService.sh -s webfrontend
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
#### Orchestrator
```
./DeprovisionService.sh -s orchestrator
```
#### Remote Data Connector
```
./DeprovisionService.sh -s remotedataconnector
```
#### Secure Computation Node
```
./DeprovisionService.sh -s securecomputationnode
```
#### Web Frontend
```
./DeprovisionService.sh -s webfrontend
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
