#!/bin/bash

cd /app || exit
./RestApiPortal 2>&1 | tee restportal.log &

pushd Email
uvicorn main:emailPlugin --host 0.0.0.0 2>&1 | tee email.log &
popd

pushd DatasetFast
uvicorn main:server --port 6001 --host 0.0.0.0 2>&1 | tee DatasetFast.log &
popd

tail -f /dev/null
