#!/bin/bash

#package necessary files and dirs
tar -zcvf package.tar.gz series.py test_server.py dataframe.py custom_typing.py private_keys public_keys zero

#move the package to Binary
mkdir -p ../Binary/rpcrelated_dir/
mv ./package.tar.gz ../Binary/rpcrelated_dir/
