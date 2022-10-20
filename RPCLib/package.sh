#!/bin/bash

#package necessary files and dirs
tar -zcvf package.tar.gz test_server.py private_keys public_keys zero ../../datascience/sail-safe-functions

#move the package to Binary
mkdir -p ../Binary/rpcrelated_dir/
mv ./package.tar.gz ../Binary/rpcrelated_dir/
