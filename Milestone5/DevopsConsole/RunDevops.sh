#!/bin/bash
set -e

# Check if docker is installed
docker --version
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error docker does not exist"
    exit $retVal
fi

# Build the docker image
docker build . -t nginx

# Run the docker container
docker run \
  -it \
  --rm \
  -v $(pwd):/app \
  -v $(pwd)/nginx:/etc/nginx/conf.d \
  -v $(pwd)/certs:/etc/nginx/certs \
  -p 8080:443 \
  --name devops \
  nginx
