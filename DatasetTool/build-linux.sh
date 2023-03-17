#!/bin/bash

# build a dotnet binary
dotnet publish -c Release -r linux-x64

# install deb package build dep
dotnet tool install --global dotnet-deb
dotnet deb install
dotnet deb

# create a directory to store the build package
build_dir=SAILDatasetUpload-linux-x64
rm -rf $build_dir
mkdir $build_dir

# copy the release to the new directory
cp ./bin/Debug/net6.0/linux-x64/DatasetTool.1.0.0.linux-x64.deb $build_dir

# also package the sample data for consumer to try with
cp -r SampleData $build_dir

tar -cvzf $build_dir.tar $build_dir

