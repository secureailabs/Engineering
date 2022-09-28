#!/bin/bash
set -e
imageName=rpcrelated

cd /app || exit

# Start the nginx server
nginx -g 'daemon off;' 2>&1 | tee /app/nginx.log &

# vm_initializer will download the package.tar.gz and InitializationVector.json
# if they are not already present on the file system.
# Forcing a zero exit status as the api server is killed from within and there is no graceful way to do this.
python3 vm_initializer.py || true
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi

# Unpack the tar package
tar -xf package.tar.gz

# Move the InitializerVector to the Binary folder
# mv InitializationVector.json ApiServices/

# Install the rpc library
pip3 install /app/zero/zero

# Start the rpc server
python3 /app/test_server.py 5556

# To keep the container running
tail -f /dev/null
