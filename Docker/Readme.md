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
./RunService.sh -s backend
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
### Shutdown and Deprovision services

#### All Docker
```
./DeprovisionService.sh -s all
```
*Alternatively, you can add DeprovisionService.sh to pathvia symbolic link and trigger from anywhere!*
```
eg: 
echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/bin
cd /bin
ln -s <abs_path>/Engineering/Docker/DeprovisionService.sh .
```
#### Backend
```
./DeprovisionService.sh -s backend
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

#### Note:
1. Use the `-d` flag to run the services in the background in docker detached mode.
2. To access the backend portal from any other container use `backend` as a domain name. e.g. the frontend webApp must connect to `https://backend:6200` instead of `https://127.0.0.1:6200/`
3. Remember you can add DeprovisionService.sh to path and run it from anywhere !!  via `DeprovisionService.sh -s all`
