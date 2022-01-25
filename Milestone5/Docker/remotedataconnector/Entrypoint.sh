#!/bin/bash

cd /app
./RemoteDataConnector
tail -f /dev/null
