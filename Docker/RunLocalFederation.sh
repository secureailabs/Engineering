#!/bin/bash
set -e

PrintHelp() {
    echo ""
    echo "Usage: $0 -d [Test Package Path] "
    echo -e "\t-d Path to the test package (Zip containing multiple datasets"
    exit 1 # Exit script after printing help
}

# Parse the input parameters
test_package=""
while getopts "d:" opt; do
    case "$opt" in
    d) test_package="$OPTARG" ;;
    ?) PrintHelp ;;
    esac
done

if [ -z $test_package ]; then
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
    dir_name=local_federation/$scn_name
    mkdir -p $dir_name
    mv local_dataset/$dataset $dir_name/
    echo "Launching SCN $scn_name"
    sed "s/LOCAL_DATASET_NAME/$dataset/g" rpcrelated/InitializationVector_local.json > rpcrelated/InitializationVector.json
    cat rpcrelated/InitializationVector.json
    ./RunService.sh -s rpcrelated -l `pwd`/$dir_name -n $scn_name -d
    if [ -z $scn_names ]; then
        scn_names="$scn_name"
    else
        scn_names+=",$scn_name"
    fi
    # Give the SCN time to come alive
    sleep 15;
done

echo $scn_names

./RunService.sh -s smart_broker -x "$scn_names"

