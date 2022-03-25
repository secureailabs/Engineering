#!/bin/bash

cd /app || exit
./RestApiPortal 2>&1 | tee restportal.log &

pushd Email
uvicorn main:emailPlugin --host 0.0.0.0 2>&1 | tee email.log &
popd

tail -f /dev/null
