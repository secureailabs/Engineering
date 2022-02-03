#!/bin/bash

cd /app || exit
./CommunicationPortal 2>&1 | tee computation.log &
tail -f /dev/null
