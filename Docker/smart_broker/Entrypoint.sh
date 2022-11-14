#!/bin/bash
set -e
imageName=rpcrelated

cd /app || exit


ls /app/zero
ls -l /app/
# Install the rpc library
pip3 install /app/zero

# Start the test script
python3 /app/rpc_test.py

# To keep the container running
tail -f /dev/null

