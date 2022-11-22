#!/bin/bash
set -e

PrintHelp() {
    echo ""
    echo "Usage: $0 -d [Test Package Path] -r [DS Repo Path]"
    echo -e "\t-d Path to the test package (Zip containing multiple datasets)"
    echo -e "\t-r Path to the DS repo to use for SCNs"
    exit 1 # Exit script after printing help
}

# Parse the input parameters
test_package=""
dsRepo=""
while getopts "r:d:" opt; do
    case "$opt" in
    d) test_package="$OPTARG" ;;
    r) dsRepo="$OPTARG" ;;
    ?) PrintHelp ;;
    esac
done

if [ -z $test_package ] || [ -z $dsRepo ]; then
    PrintHelp
fi

echo "Provisioning Docker Federation with test pacakge $test_package"

# First step unzip the test package to a local directory
mkdir -p local_dataset/
unzip $test_package -d local_dataset/

datasets=`ls local_dataset/`
scn_names=""
# Iterate through the datasets in the test package
for dataset in $datasets; do
    scn_name=scn_`basename $dataset .zip`
    container_id=`docker ps -qa --filter "name=$scn_name"`
    echo $container_id
    if [ -n "$container_id" ]; then
        echo "Container $scn_name already exists, shutting down and restarting"
        docker stop $scn_name
        docker rm $scn_name
    fi
    dir_name=local_federation/$scn_name
    mkdir -p $dir_name
    mv local_dataset/$dataset $dir_name/
    echo "Launching SCN $scn_name"
    sed "s/LOCAL_DATASET_NAME/$dataset/g" rpcrelated/InitializationVector_local.json > rpcrelated/InitializationVector.json
    cat rpcrelated/InitializationVector.json
    ./RunService.sh -s rpcrelated -l `pwd`/$dir_name -n $scn_name -r $dsRepo -d
    if [ -z $scn_names ]; then
        scn_names="$scn_name"
    else
        scn_names+=",$scn_name"
    fi
    # Give the SCN time to come alive
    sleep 15;
done

echo $scn_names

./RunService.sh -s smart_broker -r $dsRepo -x "$scn_names"

rm -rf local_dataset
rm -rf local_federation
