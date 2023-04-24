#!/usr/bin/env bash

# Test if dotnet is installed
if ! command -v dotnet &> /dev/null
then
    echo "dotnet could not be found. Please install dotnet. Instructions can be found in the Readme.md file."
    exit
fi

# Publish the dataset tool
dotnet publish -c Release

# Check of the dataset tool is published
if [ ! -f "bin/Release/net6.0/linux-x64/publish/DatasetTool" ]; then
    echo "The dataset tool could not be published. Please check the Readme.md file for instructions."
    exit
fi

# Run the dataset tool for IGR dataset
bin/Release/net6.0/linux-x64/publish/DatasetTool --email lbart@igr.com --password SailPassword@123 --config SampleData/igr_config.json --ip 172.20.100.11:8000

# Run the dataset tool for MGR dataset
bin/Release/net6.0/linux-x64/publish/DatasetTool --email nadams@mghl.com --password SailPassword@123 --config SampleData/mghl_config.json --ip 172.20.100.11:8000

# Run the dataset tool for SJC dataset
bin/Release/net6.0/linux-x64/publish/DatasetTool --email michael@saintjacob.org --password SailPassword@123 --config SampleData/sjc_config.json --ip 172.20.100.11:8000
