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
# Iterate through the datasets in the test package
for dataset in $datasets; do
    dir_name=scn_`basename $dataset .zip`
    mkdir -p $dir_name
    mv local_dataset/$dataset $dir_name/
    echo "Launching SCN $dir_name"
    ./RunService.sh -s rpcrelated -l $dir_name -n $dir_name -d
done
    # For each dataset call RunService with a unique name for the dataset

# Start the smart broker
sleep 30