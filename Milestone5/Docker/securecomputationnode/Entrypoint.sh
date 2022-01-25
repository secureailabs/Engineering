#!/bin/bash

cd /app
./CommunicationPortal 2>&1 | tee computation.log &
tail -f /dev/null
