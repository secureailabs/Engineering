#!/bin/bash

cd /app || exit
./RemoteDataConnector
tail -f /dev/null
