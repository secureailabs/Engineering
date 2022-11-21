#!/bin/bash
set -e
imageName=rpcrelated

cd /app || exit

# Install the rpc library
pip3 install /app/zero
pip3 install /ds/sail-safe-functions
pip3 install /ds/sail-safe-functions-orchestrator
pip3 install /ds/sail-safe-functions-test

pip3 install /ds/helper-libs

# Start the orchestrator test
PATH_DIR_PUBLIC_KEY_ZEROMQ=/app/public_keys/ PATH_FILE_PRIVATE_KEY_ZEROMQ_CLIENT=/app/private_keys/client.key_secret PATH_DIR_DATASET=/data/ python3 /ds/sail-safe-functions-test/integration_test/test_orchestrator_1.py

# To keep the container running
tail -f /dev/null

