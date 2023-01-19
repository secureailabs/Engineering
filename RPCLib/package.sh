#!/bin/bash

#package necessary files and dirs
tar --exclude='datascience/**venv**' --exclude='datascience/sail-safe-functions-test/sail_safe_functions_test/data_sail_safe_functions' --exclude='datascience/**pycache**' --exclude='datascience/.git' --exclude='datascience/.github' -zcvf package.tar.gz promtail_linux_amd64 promtail_local_config.yaml test_server.py private_keys public_keys zero ../datascience

#move the package to Binary
mkdir -p ../Binary/rpcrelated_dir/
mv ./package.tar.gz ../Binary/rpcrelated_dir/
