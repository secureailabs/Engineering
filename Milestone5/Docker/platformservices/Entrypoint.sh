#!/bin/bash

cd /app || exit
./RestApiPortal 2>&1 | tee restportal.log &
tail -f /dev/null
