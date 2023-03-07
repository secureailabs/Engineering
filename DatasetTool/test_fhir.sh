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

# Unpack the SampleFhir dataset
unzip SampleFhir/patient_data.zip -d SampleFhir/

# Run the dataset tool for IGR dataset
bin/Release/net6.0/linux-x64/publish/DatasetTool --email nadams@mghl.com --password SailPassword@123 --config SampleFhir/igr_config.json --ip 172.20.100.7:8000

# Run the dataset tool for IGR dataset
bin/Release/net6.0/linux-x64/publish/DatasetTool --email lbart@igr.com --password SailPassword@123 --config SampleFhir/mghl_config.json --ip 172.20.100.7:8000

rm -rf SampleFhir/patient_data
