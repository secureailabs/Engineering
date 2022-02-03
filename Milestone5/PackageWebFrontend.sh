#!/bin/bash

pushd WebFrontend/client
rm -rf node_modules
popd

pushd WebFrontend/server
rm -rf node_modules
popd

# Compress and package all the files
tar -czvf WebFrontend.tar.gz WebFrontend
